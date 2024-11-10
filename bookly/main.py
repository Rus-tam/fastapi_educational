from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
async def read_root() -> dict:
    return {"message": "Hello world"}

@app.get('/greet/{name}/{age}')
async def greet_name(name: str, age: int) -> dict:
    return {"message": f"Hello, {name}. Age {age}"}


class BookCreateModel(BaseModel):
    title: str
    author: str

@app.post('/create_book')
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }