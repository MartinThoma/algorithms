# Core Library modules
from typing import List

# First party modules
from orms2 import Author, Book, db_connection


@db_connection
def get_titles_by_authors(session, author_ids: List[int]) -> List[str]:
    books = session.query(Book.title).filter(Book.author_id.in_(author_ids)).all()
    return [book.title for book in books]


if __name__ == "__main__":
    print(get_titles_by_authors([1, 2]))
