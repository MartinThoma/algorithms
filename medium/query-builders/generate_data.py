import random
from faker import Faker
from dataclasses import dataclass

fake = Faker()


@dataclass
class Author:
    id: int
    first_name: str
    last_name: str


@dataclass
class Book:
    id: str
    title: str
    original_language: str
    author: Author
    isbn: str


def generate_books():
    book_id = 0
    author_id = 0
    author_id2author = {}
    while True:
        title = fake.name()
        original_language = random.choice(["DE", "EN", "RU", "FR"])

        first_name = fake.first_name()
        last_name = fake.last_name()
        book_id += 1
        if random.random > 0.6:
            author_id += 1
            author = Author(author_id, first_name, last_name)
        else:
            known_id = random.choice(author_id2author.keys())
            author = author_id2author[known_id]
        yield Book(book_id, title, original_language, author, isbn=fake.isbn13())


book = generate_user()
print(book)
