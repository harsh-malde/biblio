from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str

class BookOut(BaseModel):
    id: int
    title: str
    author: str

books_db = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction"},
    {"id": 3, "title": "1984", "author": "George Orwell", "genre": "Dystopian"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance"},]

@app.get("/")
def welcome():
    return {"message" : "Welcome to Biblio!"}

@app.get("/health")
def health():
    return {"status" : "healthy"}

@app.get("/books", response_model=list[BookOut])
def get_books(genre: str | None = None):
    if genre:
        return [book for book in books_db if book["genre"].lower() == genre.lower()]
    return books_db

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", status_code = 201, response_model= BookOut)
def create_book (book: BookCreate):
    new_book = book.model_dump()
    biggest_id = max(b["id"] for b in books_db) if books_db else 0
    new_book["id"] = biggest_id + 1
    books_db.append(new_book)
    
    return new_book

@app.delete("/books/{book_id}", status_code = 204)
def delete_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            books_db.remove(book)
            return
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated_book: BookCreate):
    for book in books_db:
        if book["id"] == book_id:
            book.update(updated_book.model_dump())
            return book
    raise HTTPException(status_code=404, detail="Book not found")