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
