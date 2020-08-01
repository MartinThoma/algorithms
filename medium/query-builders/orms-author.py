# Core Library modules
from typing import List

# First party modules
from orms2 import Author, Book, db_connection


@db_connection
def get_titles_by_authors(session, author_ids: List[int]) -> List[str]:
    all_titles = []
    for author_id in author_ids:
        books = session.query(Book.title).filter(Book.author_id == author_id).all()
        print(books)
        all_titles += [book.title for book in books]
    return all_titles


if __name__ == "__main__":
    print(get_titles_by_authors([1, 2]))
