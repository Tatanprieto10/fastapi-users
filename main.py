from fastapi import FastAPI
from routers import users, single_user, movies, single_movie, login
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Accessible addresses 
origin = [
  'http://localhost:3000'
]

# CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=origin,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=["*"]
)

## Routers
app.include_router(users.users_router)
app.include_router(single_user.router)
app.include_router(movies.router)
app.include_router(single_movie.router)
app.include_router(login.router)


## functions 

@app.get("/")
def root():
  return 'This is the First test for the user API. In this API we will find testing information from fake users that is made to model a users API'