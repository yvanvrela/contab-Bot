from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values("api/.env")

conn = MongoClient(config['MONGO_URI'])