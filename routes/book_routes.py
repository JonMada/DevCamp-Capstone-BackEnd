from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from models import Book, User
from schemas import BookCreate, Book as BookSchema
from database import get_db
from auth import get_current_user

router = APIRouter()

# Crear un libro
@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = Book(**book.dict(), owner_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Obtener todos los libros
@router.get("/", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

# Obtener libros por usuario
@router.get("/my_books", response_model=List[Book])
def get_books_by_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Book).filter(Book.owner_id == current_user.id).all()

# Leer un libro por ID
@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Actualizar un libro
@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id, Book.owner_id == current_user.id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

# Borrar un libro
@router.delete("/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id, Book.owner_id == current_user.id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book