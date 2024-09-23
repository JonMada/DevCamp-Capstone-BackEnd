from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from models import Book, User
from schemas import BookCreate, Book as BookSchema
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.post("/", response_model=BookSchema)
async def create_book(
    book: BookCreate,
    cover_image: UploadFile = File(...),  # Cambia a UploadFile
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Lee el contenido del archivo
    cover_image_bytes = await cover_image.read()

    db_book = Book(
        title=book.title,
        author=book.author,
        year_published=book.year_published,
        cover_image=cover_image_bytes,  # Asigna los bytes leídos
        summary=book.summary,
        review=book.review,
        rating=book.rating,
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
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id, Book.owner_id == current_user.id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
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
