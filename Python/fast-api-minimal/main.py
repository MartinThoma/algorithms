from typing import Optional

from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


class Book(BaseModel):
    title: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, q: Optional[str] = None):
    return Book(title=f"Item {book_id}")


@app.post("/books/{book_id}")
def create_book(book_id: int, item: Book):
    print(item)
    print(book_id)
    return item
