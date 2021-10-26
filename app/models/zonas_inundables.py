from sqlalchemy.orm import relationship
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_

class ZonaInundable(db.model):
    """
    
    """
    __tablename__ = 'zonasInundables'
    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True)
    name = Column(String(255), unique=True)
    coords = Column(String(255), unique=True)
    state = Column(Boolean, default=False)
    color = Column(String(255))

    coords = relationship('coordenadas', secondary='zona_tiene_coords', backref='zonasInundables')