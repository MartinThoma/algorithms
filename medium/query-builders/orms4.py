# Core Library modules
from typing import List

# First party modules
from orms2 import Author, Book, db_connection


@db_connection
def get_titles_by_author(session, author_id: int) -> List[str]:
    books = session.query(Book.title).filter(Book.author_id == author_id).all()
    return [book.title for book in books]


if __name__ == "__main__":
    print(get_titles_by_author(1))
