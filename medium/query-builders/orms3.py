# Core Library modules
from typing import List

# First party modules
from orms2 import Author, Book, db_connection
# Third party modules
from sqlalchemy.orm import joinedload


@db_connection
def get_titles_by_author(session, author_id: int) -> List[str]:
    author = (
        session.query(Author)
        .filter(Author.id == author_id)
        .options(joinedload(Author.books).load_only(Book.title),)
        .one()
    )
    return [book.title for book in author.books]


if __name__ == "__main__":
    print(get_titles_by_author(1))
