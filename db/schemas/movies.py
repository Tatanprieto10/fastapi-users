def movie_schema(movie) -> dict:
  return {
    key: value
    for key, value in {
      "id": str(movie.get("_id")),
      "name": movie.get("name"),
      "duration": movie.get("duration"),
      "gender": movie.get("gender")
    }.items()
    if value is not None and value != ""
  }

def movies_schema(movies) -> list:
  return [movie_schema(movie) for movie in movies]