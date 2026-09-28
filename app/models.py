from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class BooksDB(Base):
   
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(255), nullable=False)