from pymongo import MongoClient
from flask import current_app
from urllib.parse import quote_plus

username = "erpSystem"
password = quote_plus("CQERPSys@01")
cluster_url = "mediguide.hg27h.mongodb.net"
db_name = "MediGuide"

uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority&appName={db_name}"

client = MongoClient(uri)

def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mediguideai_db"]
    return db

def create_user(username, password):
    db = get_db()
    users_collection = db["users"]

    if users_collection.find_one({"username": username}):
        return "User already exists"
    
    users_collection.insert_one({"username": username, "password": password})
    return "User created successfully"

def authenticate_user(username, password):
    db = get_db()
    users_collection = db["users"]
    
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return True
    return False
