from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional, List
from fastapi.exceptions import HTTPException
from random import randrange


app = FastAPI()


class Post(BaseModel):
    id: int
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
    return my_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return post_dict


@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            my_posts.remove(post)
            return {"message": "Post successefully delated"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, update_post: Post):
    post_dict = update_post.dict()
    post_dict["id"] = id

    index = 0
    for post in my_posts:
        if post["id"] == id:
            index = my_posts.index(post)
            my_posts[index] = post_dict
            return post_dict

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
