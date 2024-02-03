from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from db.models.movie_models import Movie
from db.client import db_client
from db.schemas.movies import movie_schema
from bson import ObjectId


router = APIRouter(
  prefix="/movie",
  tags=["movie"],
  responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}}
)

@router.get("/{id}")
async def movie(id: str):
  return search_movie("_id", ObjectId(id))



@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def movie(movie: Movie):
  if type(search_movie("name", movie.name)) == Movie:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Movie already exists"})
  
  movie_dict = dict(movie)
  del movie_dict["id"]

  if movie_dict["gender"] == None:
    del movie_dict["gender"]

  id = db_client.movies.insert_one(movie_dict).inserted_id

  new_movie = db_client.movies.find_one({"_id": id})

  return Movie(**new_movie)


@router.put("/", response_model=Movie, status_code=status.HTTP_202_ACCEPTED)
async def movie(movie: Movie):
  movie_dict = dict(movie)
  del movie_dict["id"]

  try:
    db_client.movies.find_one_and_replace({"_id": ObjectId(movie.id)}, movie_dict)
  except:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found - not updated")


def search_movie(field: str, key):
  try:  
    movie = db_client.movies.find_one({field: key})

    if movie:
      return JSONResponse(content=movie_schema(movie))
  except:
    return {"error": "Movie Not Found"}