from fastapi import FastAPI, status, Response
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime


app = FastAPI()


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi_db",
            user="postgres",
            password="root",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to db failed")
        print("Error: ", error)
        time.sleep(2)


my_posts: List[Post] = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


@app.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
async def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()

    conn.commit()

    return new_post


@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, updates: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
        (updates.title, updates.content, updates.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )

    return updated_post
