from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int]

@app.get("/")
async def root():
    return {"Welcome": "TO My API"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/posts")
def create_post(new_post: Post):
    print(new_post.title)
    return{"data": "new post", }

    