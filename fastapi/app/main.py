from fastapi import FastAPI, status, Response, Depends
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .types import Post


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
def get_postst(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )

    updated_post.id = post.id

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post
