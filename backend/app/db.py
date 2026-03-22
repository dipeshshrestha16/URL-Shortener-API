from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['url_shortener']
collection = db['urls']