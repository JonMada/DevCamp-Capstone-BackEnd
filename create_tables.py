from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL = "postgresql://etxelit_db_user:6o3QBA70ph1xhIf2169I7C8n01xdDOZP@dpg-crlfv4t6l47c7382a8ag-a.oregon-postgres.render.com/etxelit_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Definición del modelo User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    
    # Relación con el modelo Book
    books = relationship("Book", back_populates="owner")

# Definición del modelo Book
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
    
    # Relación con el modelo User
    owner = relationship("User", back_populates="books")

# Crear todas las tablas en la base de datos
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
