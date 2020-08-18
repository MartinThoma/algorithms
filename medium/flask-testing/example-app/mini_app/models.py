# Core Library modules
from typing import Dict, Union

# First party modules
from mini_app.app import db
# Third party modules
from sqlalchemy import ForeignKey


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    def dict(self) -> Dict[str, Union[int, str]]:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, ForeignKey("authors.id"), nullable=False)
    title = db.Column(db.Text)
    original_language = db.Column(db.Text)
    isbn = db.Column(db.Text)
