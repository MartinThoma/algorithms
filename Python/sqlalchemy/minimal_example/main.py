import datetime
import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "sqlite:///foobar.db"

# Cleanup for this example
if os.path.isfile(SQLALCHEMY_DATABASE_URI):
    os.remove(SQLALCHEMY_DATABASE_URI)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)


Base.metadata.create_all(engine)

me = User(name="Martin", fullname="Martin Thoma")
session.add(me)
john_snow = User(name="John", fullname="John Snow")
session.add(john_snow)
session.commit()


def db_backup(session, Model, dump_path=None):
    from sqlalchemy.ext.serializer import dumps

    if dump_path is None:
        now = datetime.datetime.now()
        dump_path = os.path.abspath(f"dump_{now:%Y-%m-%d-%H%M%S}.pickle")
    q = session.query(Model).all()
    serialized_data = dumps(q)
    with open(dump_path, "wb") as f:
        f.write(serialized_data)
    return dump_path


db_backup(session, User)
