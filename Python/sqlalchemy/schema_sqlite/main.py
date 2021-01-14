import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "sqlite:///foobar.db"

Base = declarative_base()
user = sa.Table(
    "users", Base.metadata, sa.Column("id", sa.Integer, primary_key=True), schema="foobar"
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base.metadata.create_all(engine)
