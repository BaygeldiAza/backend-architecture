from fastapi import FastAPI, Response, status, HTTPException
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
        
def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i  

@app.get("/")
async def root():
    return {"Welcome": "TO My API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f"post with {id} not found"})
    return{"post detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    new_post_dict = new_post.dict()
    new_post_dict['id'] = randrange(0,1000000)
    my_posts.append(new_post_dict)
    return{"data": new_post_dict}

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"post {id} is not found"})
    post_dict=post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': my_posts}

@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
def  delete_all():
    if len(my_posts) == 0 :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    
    my_posts.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f"post with {id} not found"})
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    

