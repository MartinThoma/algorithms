# Core Library modules
import os
from typing import List

# Third party modules
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def db_connection(f):
    """
    Supply the decorated function with a database connection.

    Commit/rollback and close the connection after the function call.
    """

    def with_connection_(*args, **kwargs):
        # https://martin-thoma.com/sql-connection-strings/
        user = os.environ["DB_USER"]
        password = os.environ["DB_PASSWORD"]
        engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost/books")
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            rv = f(session, *args, **kwargs)
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()
        finally:
            session.close()

        return rv

    return with_connection_


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer)


@db_connection
def get_titles_by_author(session, author_id: int) -> List[str]:
    books = session.query(Book).filter(Book.author_id == author_id).all()
    return [book.title for book in books]


if __name__ == "__main__":
    print(get_titles_by_author(1))
