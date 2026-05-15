from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"Welcome": "TO My API"}

@app.get("/items/{item_id}")
async def read_items(item_id: int, q: str | None=None):
    return {"item_id": item_id, "q": q}

@app.post("/createposts")
def create_post(posts: dict = Body(...)):
    return{"new_post": f"title {posts.title} content: {posts.content}"}