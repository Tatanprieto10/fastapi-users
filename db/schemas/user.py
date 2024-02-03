def user_schema(user) -> dict:
  return {
    key: value
    for key, value in {
      "id": str(user.get("_id")),
      "username": user.get("username"),
      "name": user.get("name"),
      "lastname": user.get("lastname"),
      "email": user.get("email"),
      "salary": user.get("salary"),
      "movies": user.get("movies")
    }.items()
    if value is not None
  }

def users_schema(users) -> list:
  return [user_schema(user) for user in users]