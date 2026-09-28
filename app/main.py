from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from .database import engine, Base, get_db
from sqlalchemy.orm import Session
from .models import BooksDB

Base.metadata.create_all(bind=engine)

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: str
    genre: str

@app.get("/")
def welcome():
    return {"message" : "Welcome to Biblio!"}

@app.get("/health")
def health():
    return {"status" : "healthy"}

@app.get("/books", response_model=list[BookOut])
def get_books(genre: str | None = None, db: Session = Depends(get_db)):
    query = db.query(BooksDB)
    if genre:
        query = query.where(BooksDB.genre.ilike(genre))
    return query.all()

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BooksDB, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", status_code = 201, response_model= BookOut)
def create_book (book: BookCreate, db: Session = Depends(get_db)):
    new_book = BooksDB(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.delete("/books/{book_id}", status_code = 204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(BooksDB, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()

@app.put("/books/{book_id}", response_model=BookOut)
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