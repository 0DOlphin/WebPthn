from sqlalchemy import Integer, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from ..extensions import db

class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[date] = mapped_column(Date, nullable=True) 
    complete: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('category.id', name='fk_category'), nullable=True)

class Category(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    todos = db.relationship('Todo', backref='category')
