from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BooksDB
from ..schemas import BookCreate, BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", response_model=list[BookOut])
def get_books(genre: str | None = None, db: Session = Depends(get_db)):
    query = db.query(BooksDB)
    if genre:
        query = query.where(BooksDB.genre.ilike(genre))
    return query.all()

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BooksDB, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("", status_code=201, response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = BooksDB(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BooksDB, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    book = db.get(BooksDB, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = updated_book.title
    book.author = updated_book.author
    book.genre = updated_book.genre
    db.commit()
    db.refresh(book)
    return book