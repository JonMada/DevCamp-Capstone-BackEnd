from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://etxelit_database_user:XxqZe7wJxhv6SnWHhnv4UQsyVbDJJN3R@dpg-crq77dqj1k6c738cce50-a.oregon-postgres.render.com/etxelit_database"
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    
    
    books = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    year_published = Column(Integer)
    cover_image = Column (String(255))
    summary = Column(Text)
    review = Column(Text)
    rating = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    
    owner = relationship("User", back_populates="books")


def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
