from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from .database.db import engine, get_db
from .models import models
from .schemas.schemas import PostCreate, Post


#while True:
#    try:
#        conn = psycopg2.connect(host = 'localhost', database='backend-architecture', user='postgres',
#                            password = 'BAY_18geldi_18', cursor_factory=RealDictCursor)
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

@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    return posts 
    

@app.get("/posts/{id}",response_model=Post)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} is not found")
    return post 

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts(title, content, is_published) VALUES (%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/posts/{id}",response_model=Post)
def update_post(id:int, posts: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not found")
    
    post_query.update(posts.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def  delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} is not found"
        )
    db.delete(deleted_post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)