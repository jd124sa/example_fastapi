from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from . import models
# from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# creates all dabases set in the models.py fileu using sqlalchemy
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="App", redirect_slashes=False)

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB  connection with psycopg2

# imports the routs from ./routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# root
@app.get("/")
def root():
    return {"message": "welcome"}
