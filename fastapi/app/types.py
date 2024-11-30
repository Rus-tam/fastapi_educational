from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
