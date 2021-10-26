import datetime
from sqlalchemy.orm import relationship
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_, Float

class Denuncia(db.model):
    """
    
    """
    __tablename__ = 'denuncias'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    category = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime, default=None)
    description = Column(String(255), unique=True)
    lat = Column(String(255))
    long = Column(String(255))
    state = Column(String(255))
    assigned_to = Column(Integer, ForeignKey('users.id'))
