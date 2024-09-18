from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from models import Book as BookModel, User as UserModel
from schemas import BookCreate, Book as BookSchema
from database import get_db
from auth import get_current_user

router = APIRouter()

# Crear un libro
@router.post("/", response_model=BookSchema)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_book = BookModel(**book.dict(), owner_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookSchema.from_orm(db_book)

# Obtener todos los libros
@router.get("/", response_model=List[BookSchema])
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return [BookSchema.from_orm(book) for book in books]

# Obtener libros por usuario
@router.get("/my_books", response_model=List[BookSchema])
def get_books_by_user(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    books = db.query(BookModel).filter(BookModel.owner_id == current_user.id).all()
    return [BookSchema.from_orm(book) for book in books]

# Leer un libro por ID
@router.get("/{book_id}", response_model=BookSchema)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookSchema.from_orm(book)

# Actualizar un libro
@router.put("/{book_id}", response_model=BookSchema)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id, BookModel.owner_id == current_user.id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return BookSchema.from_orm(db_book)

# Borrar un libro
@router.delete("/{book_id}", response_model=BookSchema)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id, BookModel.owner_id == current_user.id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return BookSchema.from_orm(db_book)
