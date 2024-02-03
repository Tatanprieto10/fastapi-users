from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from db.models.movie_models import Movie
from db.client import db_client
from db.schemas.movies import movies_schema


router = APIRouter(
  prefix="/movies",
  tags=["movies"],
  responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}}
)

@router.get("/", response_model=list[Movie])
async def movies():
  movies_data = db_client.movies.find()

  if movies_data:
    return JSONResponse(content=movies_schema(movies_data), status_code=status.HTTP_200_OK)
  
  return JSONResponse(content={"error": "Not data found"})