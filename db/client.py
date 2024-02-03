## manage the connection to MongoDB

from pymongo import MongoClient
from dotenv import load_dotenv
import os


## Local database
#db_client = MongoClient().local


# Cloud database

load_dotenv()
MONGO_URI = os.environ.get("DB_STRING")
db_client = MongoClient(MONGO_URI).MongoSebasP