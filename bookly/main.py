from fastapi import FastAPI, Header, status
from fastapi.exceptions import HTTPException
from typing import Optional
from pydantic import BaseModel
from typing import List

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1",
        "publisher": "Publisher 1",
        "published_data": "Published data 1",
        "page_count": 1234,
        "language": "English"
    },
    {
        "id": 2,
        "title": "Book 2",
        "author": "Author 2",
        "publisher": "Publisher 2",
        "published_data": "Published data 2",
        "page_count": 4321,
        "language": "English"
    },
        {
        "id": 3,
        "title": "Book 3",
        "author": "Author 3",
        "publisher": "Publisher 3",
        "published_data": "Published data 3",
        "page_count": 5678,
        "language": "English"
    },
        {
        "id": 4,
        "title": "Book 4",
        "author": "Author 4",
        "publisher": "Publisher 4",
        "published_data": "Published data 4",
        "page_count": 9432,
        "language": "English"
    },
]

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_data: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books

@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: Book):
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book

@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.patch("/book/{book_id}", status_code=status.HTTP_201_CREATED, response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')