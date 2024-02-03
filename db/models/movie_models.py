from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
  id: Optional[str] = None
  name: str
  duration: int
  gender: Optional[str] = None