from pymongo import MongoClient

client  = MongoClient("mongodb://mongo:27017/")
db = client["url-shortener"]
collection = db["urls"]

