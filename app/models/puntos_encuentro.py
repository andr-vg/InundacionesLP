import datetime

from app.db import db
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import relationship


class PuntosDeEncuentro(db.Model):
    @classmethod
    def get_all(cls):
        return PuntosDeEncuentro.query.all()

    @classmethod
    def search_by_name(cls, name):
        return PuntosDeEncuentro.query.filter(PuntosDeEncuentro.name.like('%'+name+'%'))


    @classmethod
    def unique_fields(cls,params):
        punto_encuentro = PuntosDeEncuentro.query.filter((PuntosDeEncuentro.name==params["name"]) | (PuntosDeEncuentro.address==params["address"])).first()
        return punto_encuentro

    __tablename__ = "puntosEncuentro"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    address = Column(String(255), unique=True)
    tel = Column(String(255))
    email = Column(String(255))
    state = Column(Boolean, default=False)
    coords = Column(String(255), unique=True)
    updated_at = Column(DateTime,onupdate=datetime.datetime.utcnow , default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, address, tel, email, coords):
        self.email = email
        self.address = address
        self.name = name
        self.tel = tel
        self.coords = coords

    def get_punto_by_id(id):
        return PuntosDeEncuentro.query.filter(PuntosDeEncuentro.id==id).first()
    

    def get_punto_by_name(name):
        return PuntosDeEncuentro.query.filter(PuntosDeEncuentro.name==name.upper()).first()

    
    def get_punto_by_address(address):
        return PuntosDeEncuentro.query.filter(PuntosDeEncuentro.address==address.upper()).first()