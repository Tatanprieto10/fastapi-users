## manage the connection to MongoDB

from pymongo import MongoClient


## Local database
#db_client = MongoClient().local


# Cloud database

MONGO_URI = "mongodb+srv://tsting_user:testinguser@mongosebasp.ozcuobk.mongodb.net/?retryWrites=true&w=majority"
db_client = MongoClient(MONGO_URI,).MongoSebasP