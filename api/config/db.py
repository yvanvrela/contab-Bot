from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values("src/api/.env")

conn = MongoClient(config['MONGO_URI'])