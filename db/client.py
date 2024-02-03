## manage the connection to MongoDB

from pymongo import MongoClient


## Local database
#db_client = MongoClient().local


# Cloud database

MONGO_URI = "mongodb+srv://tsting_user:testinguser@mongosebasp.ozcuobk.mongodb.net/?retryWrites=true&w=majority"
db_client = MongoClient(
  MONGO_URI,
  ssl=True,
  ssl_cert_reqs=ssl.CERT_NONE,
  ssl_match_hostname=False,
  ssl_purpose=ssl.Purpose.SERVER_AUTH
).MongoSebasP