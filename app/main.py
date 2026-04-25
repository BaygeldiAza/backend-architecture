from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Fast API is running"}