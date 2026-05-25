from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .database.db import engine, get_db
from .models import models



while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='backend-architecture', user='postgres',
                            password = 'BAY_18geldi_18', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

models.Base.metadata.create_all(bind=engine)



app = FastAPI()





class Post(BaseModel):
    title: str
    content: str
    published: bool = True



@app.get("/")
async def root():
    return {"Welcome": "TO My API"}

@app.get("/sqlalchemy")
def test(Db: Session = Depends(get_db)):

    return {"data": "created successfully"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts }

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} is not found")
    return{"post detail": post }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, is_published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data": new_post}

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} is not found")
    return {'data': updated_post}

@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
def  delete_all():
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    delete_post = cursor.fetchone()
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)