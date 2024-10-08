from fastapi import APIRouter, Depends, Form, HTTPException
from typing import List
from sqlalchemy.orm import Session
from models import Book, User
from schemas import BookCreate, Book as BookSchema
from database import get_db
from auth import get_current_user


router = APIRouter()

router = APIRouter()

@router.post("/", response_model=BookSchema)
async def create_book(
    title: str = Form(...),
    author: str = Form(...),
    year_published: int = Form(None),
    summary: str = Form(None),
    review: str = Form(None),
    rating: int = Form(None),
    cover_image: str = Form(...),  
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_book = Book(
        title=title,
        author=author,
        year_published=year_published,
        cover_image=cover_image,
        summary=summary,
        review=review,
        rating=rating,
        owner_id=current_user.id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookSchema])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/my_books", response_model=List[BookSchema])
def get_books_by_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Book).filter(Book.owner_id == current_user.id).all()

@router.get("/{book_id}", response_model=BookSchema)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    year_published: int = Form(None),
    summary: str = Form(None),
    review: str = Form(None),
    rating: int = Form(None),
    cover_image: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_book = db.query(Book).filter(Book.id == book_id, Book.owner_id == current_user.id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = title
    db_book.author = author
    db_book.year_published = year_published
    db_book.summary = summary
    db_book.review = review
    db_book.rating = rating
    db_book.cover_image = cover_image

    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", response_model=BookSchema)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id, Book.owner_id == current_user.id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book
