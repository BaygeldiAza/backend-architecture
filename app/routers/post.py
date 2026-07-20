from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from ..database.db import get_db
from ..models import models
from ..schemas.schemas import Post, PostCreate, PostOut
from ..auth import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)
    # ).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post,
        func.count(models.Vote.post_id).label("votes")
        ).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True
        ).group_by(models.Post.id).filter(models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()

    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #return posts 
    return [
    {
        "post": row.Post,
        "votes": row.votes
    }
        for row in posts
    ]

@router.get("/{id}",response_model=List[PostOut])
def get_post(id:int, db: Session = Depends(get_db)):
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post,
        func.count(models.Vote.post_id).label("votes")
        ).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} is not found")
    return[
        {
            "post": post.Post,
            "votes": post.votes
        }
    ] 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts(title, content, is_published) VALUES (%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}",response_model=Post)
def update_post(id:int, posts: PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id,
                                            models.Post.owner_id == current_user.id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not found")

    post_query.update(posts.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def  delete_post(id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id, models.Post.owner_id == current_user.id).first()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} is not found"
        )
    db.delete(deleted_post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

