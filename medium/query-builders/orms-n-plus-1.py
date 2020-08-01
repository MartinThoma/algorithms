# Core Library modules
from typing import List, NamedTuple

# First party modules
from orms2 import Author, Book, db_connection


class BooksResult(NamedTuple):
    book_id: str
    title: str
    first_name: str
    last_name: str


@db_connection
def get_all_books(session) -> List[BooksResult]:
    all_books = []
    books = session.query(Book).all()
    for book in books:
        all_books.append(
            BooksResult(
                book_id=book.id,
                title=book.title,
                first_name=book.author.first_name,
                last_name=book.author.last_name,
            )
        )
    return all_books


if __name__ == "__main__":
    print(get_all_books())
