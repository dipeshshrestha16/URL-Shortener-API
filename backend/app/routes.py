from flask import Blueprint, request, jsonify, redirect
from .db import collection
from .utils import generate_code
from functools import wraps
import time

rate_limit_data ={}
MAX_REQUESTS = 5
TIME_WINDOW = 60

main = Blueprint('main', __name__)


#home route
@main.route('/')
def home():
    return "Welcome to URL shortener API, API is currently running."\
    
def rate_limiter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip= request.remote_addr
        now = time.time()

        #initialize list for this ip
        if ip not in rate_limit_data:
            rate_limit_data[ip]=[]

        #removing timestamps older than time window
        rate_limit_data[ip]= [t for t in rate_limit_data[ip] if now - t < TIME_WINDOW]

        if len(rate_limit_data[ip]) >= MAX_REQUESTS:
            retry_after = TIME_WINDOW - (now - rate_limit_data[ip][0])
            return jsonify({'error':'Rate limit exceeded','retry_after':int(retry_after)}), 429
        
        #record the request
        rate_limit_data[ip].append(now)

        return func(*args, **kwargs)
    return wrapper

#route to shorten url
@main.route('/shorten', methods=['POST'])
@rate_limiter
def shorten():
    data = request.json
    long_url = data.get('url')

    print("Recieved URL:", long_url)  # Debugging statement

    #check for duplicate urls
    existing = collection.find_one({'long_url': long_url})
    if existing:
        print("URL already exists")
        return jsonify({'short_url': f"http://localhost:5000/{existing['code']}"})
    
    while True:
        code = generate_code()
        # Check if the generated code already exists
        if not collection.find_one({'code': code}):
            break
    print("Generated code:", code) 

    collection.insert_one({'code': code, 'long_url': long_url, 'clicks':0})

    return jsonify({'short_url': f"http://localhost:5000/{code}"})

@main.route("/analytics", methods = ['GET'])
def analytics():
    urls = list(collection.find({}, {"_id" : 0, "code":1, "long_url":1, "click_times":1 }))
    for u in urls:
        if "click_times" in u:
            u["click_times"] = []
    return jsonify(urls)

#redirect to original url
@main.route('/<code>')
def redirect_url(code):
    print("Received code for redirection:", code)
    result = collection.find_one({'code': code})
    print("Database  result:", result)


    if result:
        if "clicks_times" not in result:
            result["clicks_times"] = []
            
        collection.update_one({'code': code}, {'$inc': {'clicks': 1},"$push": {"clicks_times": time.time()}})
        return redirect(result['long_url'])
    else:
        return jsonify({'error': 'URL not found'}), 404
    

    