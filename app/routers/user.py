from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from main import app
from ..database.db import get_db
from ..models import models
from ..schemas.schemas import UserBase, UserOut
from ..utils.utils import hash


@app.get("/users", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserBase ,db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}",response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exists!")
    return user

@app.put("/users/{id}")
def update_user(id: int, user: UserBase, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    users = user_query.first()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exists!")
    
    user_query.update(user.dict(),synchronize_session=False)
    db.commit()
    return user_query.first()
    