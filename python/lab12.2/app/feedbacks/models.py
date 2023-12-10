from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..extensions import db


class Feedback(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_email: Mapped[str] = mapped_column(String)
    topic: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    mark: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime) 
