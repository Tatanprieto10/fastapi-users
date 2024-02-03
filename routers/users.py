from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from db.models.users_model import User
from db.schemas.user import users_schema
from db.client import db_client

users_router = APIRouter(
  prefix='/users',
  tags=['users'],
  responses={status.HTTP_404_NOT_FOUND: {'Message': 'Not Found'}}
)

@users_router.get("/", response_model=list[User])
async def users():
  user_data = db_client.users.find()

  if user_data:
    return JSONResponse(content=users_schema(user_data), status_code=status.HTTP_200_OK)
  
  return JSONResponse(content={"message": "No list"}, status_code=status.HTTP_404_NOT_FOUND)