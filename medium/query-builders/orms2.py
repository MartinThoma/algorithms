# Core Library modules
import os
from typing import List

# Third party modules
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# First party modules
from orms import db_connection

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    books = relationship("Book")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author")


@db_connection
def get_titles_by_author(session, author_id: int) -> List[str]:
    author = session.query(Author).filter(Author.id == author_id).one()
    return [book.title for book in author.books]


if __name__ == "__main__":
    print(get_titles_by_author(1))
