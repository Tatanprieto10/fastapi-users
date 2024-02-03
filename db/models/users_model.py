from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
  id: Optional[str] = None
  username: str 
  name: str 
  lastname: str
  email: str
  salary: Optional[int] = None
  movies: Optional[list] = None

class User_db(User):
  password: str