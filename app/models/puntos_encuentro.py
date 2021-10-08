import datetime

from app.db import db
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import relationship


class PuntosDeEncuentro(db.Model):
    __tablename__ = "puntosEncuentro"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    address = Column(String(255), unique=True)
    tel = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    state = Column(Boolean, default=False)
    coords = Column(String(255), unique=True)
    updated_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, address, tel, email, coords):
        self.email = email
        self.address = address
        self.name = name
        self.tel = tel
        self.coords = coords
