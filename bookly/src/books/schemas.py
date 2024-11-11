from pydantic import BaseModel

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