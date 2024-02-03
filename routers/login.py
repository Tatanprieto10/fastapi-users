from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from db.models.users_model import User, User_db
from db.client import db_client
from datetime import datetime, timedelta, timezone

SECRET_KEY = "49fe70b9a3e889ed3adf40e76293b0cfe0b0368afce4fd376bcec7261eb7d180"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter(
  prefix="/login",
  tags=["login"],
  responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}}
)

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
  db = db_client.users.find()
  if username in db:
    user_dict = db[username]
    return User_db(**user_dict)
  
def authenticate_user(username: str, password: str):
  user = search_user_db(username)
  if not user:
    return False
  if not verify_password(password, user["password"]):
    return False
  return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expiration = datetime.now(timezone.utc) + expires_delta
  else:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=15)
  
  to_encode.update({"exp": expiration})

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: str =  payload.get("sub")
    if username is None:
      raise credentials_exception
    Token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception
  user = search_user_db(username=Token_data.username)
  if user is None:
    raise credentials_exception
  return user



@router.post("/")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> Token:
  user = authenticate_user(form.username, form.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail="Incorrect username or password", 
      headers={"WWW-Authenticate": "Bearer"}
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
  access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
  return Token(access_token=access_token, token_type="bearer")



@router.get("/me", response_model=User)
async def my_info(current_user: User = Depends(get_current_user)):
  return current_user


def search_user_db(username: str):
  return db_client.users.find_one({"username": username})