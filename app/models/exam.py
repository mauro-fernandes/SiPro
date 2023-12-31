from . import db
from sqlalchemy.sql import func
from typing import List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Exam(db.Model):
    #TODO: Add columns, etc, here
    __tablename__ = "exam"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    comments = db.Column(db.String)
    qntityOfQuestions = db.Column(db.Integer) # Quantidade de questões
    punctuation = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<exam %r>" % self.id
