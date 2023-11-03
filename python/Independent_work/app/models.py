from sqlalchemy import Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime
from app import db

class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[date] = mapped_column(Date, nullable=True) 
    complete: Mapped[bool] = mapped_column(Boolean)

class Feedback(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_email: Mapped[str] = mapped_column(String)
    topic: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    mark: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime) 
