from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/create")
async def creat_posts(post: Post):
    return {"new_post": f"title: {post.title} content: {post.content}"}
