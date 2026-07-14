from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database.db import get_db
from ..models import models
from ..schemas.schemas import UserBase, UserOut
from ..utils.utils import hash
from ..auth import oauth2

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserBase ,db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exists!")
    return user

@router.put("/{id}")
def update_user(id: int, user: UserBase, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    existing_users = user_query.first()

    if not existing_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exists!")
    user_data = user.dict()

    if "password" in user_data:
        user_data["password"] = hash(user_data["password"])

    user_query.update(user_data,synchronize_session=False)
    db.commit()
    return user_query.first()
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session=Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    deleted_user = db.query(models.User).filter(models.User.id == id).first() 
    if delete_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not found!")
    db.delete(deleted_user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)