from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    name = Column(String, primary_key=True)
    password = Column(String)


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


user = session.query(User).filter_by(name="foo").filter_by(password="bar").first()
