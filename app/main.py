from fastapi import FastAPI

import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .database.db import engine
from .models import models

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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"Welcome": "to My API"}