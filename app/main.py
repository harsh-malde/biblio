from fastapi import FastAPI
from .database import engine, Base
from .models import BooksDB
from .routers import books
from .routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)

app.include_router(users.router)

@app.get("/")
def welcome():
    return {"message": "Welcome to Biblio!"}

@app.get("/health")
def health():
    return {"status": "healthy"}