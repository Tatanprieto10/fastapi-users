from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from db.models.users_model import User, User_db
from db.client import db_client
from db.schemas.user import user_schema
from bson import ObjectId
from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


router = APIRouter(
  prefix="/user",
  tags=["user"],
  responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}}
)


@router.get("/{id}")
async def user(id: str):
  return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User_db):
  if type(search_user("email", user.email)) == User_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "User already Exists"})
  
  user_dict = dict(user)
  del user_dict["id"]

  if user_dict["salary"] == None:
    del user_dict["salary"]
    
  if user_dict["movies"] == None:
    del user_dict["movies"]

  hashed_password = get_password_hash(user_dict["password"])

  user_dict["password"] = hashed_password

  id = db_client.users.insert_one(user_dict).inserted_id

  new_user = db_client.users.find_one({"_id": id})

  return User(**new_user)


@router.put("/", response_model=User, status_code=status.HTTP_202_ACCEPTED)
async def user(user: User_db):
  user_dict = dict(user)
  del user_dict["id"]

  hashed_password = get_password_hash(user_dict["password"])

  user_dict["password"] = hashed_password

  try:
    db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
  except:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found - not updated")
  
  return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
  found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
  
  if not found:
    return {"error": "User not found to be deleted"}
  
  return {"message": "User deleted"}


def search_user(field: str, key):
  try:  
    user = db_client.users.find_one({field: key})
    
    if user:
      return JSONResponse(content=user_schema(user))
  except:
    return {"error": "User Not Found"}

def get_password_hash(password):
    return pwd_context.hash(password)