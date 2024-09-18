from sqlalchemy import Column, Integer, String, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    year_published = Column(Integer)
    cover_image = Column(LargeBinary)
    summary = Column(Text)
    review = Column(Text)
    rating = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="books")

User.books = relationship("Book", back_populates="owner")
