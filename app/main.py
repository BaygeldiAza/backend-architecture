from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int]

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "Favorite meal and fruits", "content": "Watermelon", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"Welcome": "TO My API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(new_post: Post):
    new_post_dict = new_post.dict()
    new_post_dict['id'] = randrange(0,1000000)
    my_posts.append(new_post_dict)
    return{"data": new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    return{"post detail": post}