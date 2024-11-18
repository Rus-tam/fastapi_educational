from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional, List
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts: List[Post] = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


@app.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
async def root():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def creat_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post(id: int):
    res_post: Post = {}
    for post in my_posts:
        if post["id"] == id:
            res_post = post

    return res_post
