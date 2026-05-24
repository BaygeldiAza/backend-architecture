from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='backend-architecture', user='postgres',
                            password = '----------', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True



@app.get("/")
async def root():
    return {"Welcome": "TO My API"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts }

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
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
    
    return {'data'}

@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
def  delete_all():
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    

