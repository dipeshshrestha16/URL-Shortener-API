from flask import Blueprint, request, jsonify, redirect
from .db import collection
from .utils import generate_code

main = Blueprint('main', __name__)

#home route
@main.route('/')
def home():
    return "Welcome to URL shortener API, API is currently running."\
    
#route to shorten url
@main.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    long_url = data.get('url')

    code = generate_code()

    collection.insert_one({'code': code, 'long_url': long_url})

    return jsonify({'short_url': f"http://localhost:5000/{code}"})


#redirect to original url
@main.route('/<code>')
def redirect_url(code):
    result = collection.find_one({'code': code})
    if result:
        return redirect(result['long_url'])
    else:
        return jsonify({'error': 'URL not found'}), 404
    
    