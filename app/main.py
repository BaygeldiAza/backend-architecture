from fastapi import FastAPI
from functools import lru_cache
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .database.db import engine
from .models import models
from .routers import post, user, auth, vote
from .core.config import settings
from fastapi.middleware.cors import CORSMiddleware
#while True:
#    try:
#        conn = psycopg2.connect(host = 'localhost', database='backend-architecture', user='postgres',
#                            password = 'YOUR_PASSWORD', cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
##        print("Database connection was successfull!")
#        break
#    except Exception as error:
#        print("Connecting to database failed")
#        print("Error:", error)
#      time.sleep(2)

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache
def get_settings():
    return settings


@app.get("/")
async def root():
    return {"Welcome": "Bay API "}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)