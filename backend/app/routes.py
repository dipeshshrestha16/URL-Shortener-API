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


#redirect to original url
@main.route('/<code>')
def redirect_url(code):
    print("Received code for redirection:", code)

    result = collection.find_one({'code': code})
    print("Database  result:", result)
    if result:
        collection.update_one({'code': code}, {'$inc': {'clicks': 1}})

        return redirect(result['long_url'])
    else:
        return jsonify({'error': 'URL not found'}), 404
    
    