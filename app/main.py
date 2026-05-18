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

@app.get("/items/{item_id}")
async def read_items(item_id: int, q: str | None=None):
    return {"item_id": item_id, "q": q}

@app.post("/createposts")
def create_post(new_post: Post):
    print(new_post.title)
    return{"data": "new post", }

    