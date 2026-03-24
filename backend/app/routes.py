from flask import Blueprint, request, jsonify, redirect
from .db import collection  
from functools import wraps
import time
import random
import string

main = Blueprint("main", __name__)

# Rate Limiter

rate_limit_data = {}
MAX_REQUESTS = 5
TIME_WINDOW = 60  # seconds

def rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        now = time.time()

        if ip not in rate_limit_data:
            rate_limit_data[ip] = []

        # remove old timestamps
        rate_limit_data[ip] = [t for t in rate_limit_data[ip] if now - t < TIME_WINDOW]

        if len(rate_limit_data[ip]) >= MAX_REQUESTS:
            retry_after = TIME_WINDOW - (now - rate_limit_data[ip][0])
            return jsonify({
                "error": "Rate limit exceeded",
                "retry_after": int(retry_after)
            }), 429

        rate_limit_data[ip].append(now)
        return func(*args, **kwargs)
    return wrapper


# code generator
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# api route to shorten url


@main.route("/shorten", methods=["POST"])
@rate_limiter
def shorten():
    data = request.json
    long_url = data.get("url")

    # check for duplicate
    existing = collection.find_one({"long_url": long_url})
    if existing:
        return jsonify({"short_url": f"http://localhost:5000/{existing['code']}"})

    # generate unique code
    while True:
        code = generate_code()
        if not collection.find_one({"code": code}):
            break

    collection.insert_one({
        "code": code,
        "long_url": long_url,
        "clicks": 0,
        "click_times": []
    })

    return jsonify({"short_url": f"http://localhost:5000/{code}"})


# Analytics route to check data

@main.route("/analytics", methods=["GET"])
def analytics():
    urls = list(collection.find({}, {"_id": 0, "code": 1, "long_url": 1, "click_times": 1}))
    for u in urls:
        if "click_times" not in u:
            u["click_times"] = []
    return jsonify(urls)


# Redirect endpoint

@main.route("/<code>")
def redirect_url(code):
    result = collection.find_one({"code": code})
    if result:
        # increment clicks and add timestamp
        if "click_times" not in result:
            result["click_times"] = []
        collection.update_one(
            {"code": code},
            {"$inc": {"clicks": 1}, "$push": {"click_times": int(time.time())}}
        )
        return redirect(result["long_url"])
    else:
        return "Not found", 404