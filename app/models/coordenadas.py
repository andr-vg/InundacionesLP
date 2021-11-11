
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from app.db import db
from sqlalchemy import cast, Column, Integer, String, DateTime, Boolean, text, select, and_,or_, Float
from app.models.zonas_inundables import ZonaInundable
from app.models.recorridos_evacuacion import Recorridos

class Coordenadas(db.Model):
    """
    
    """
    @classmethod
    def add_coords(cls,coords):
        db.session.add(coords)


    @classmethod
    def update_coords(cls):
        db.session.commit()

    
    @classmethod
    def get_or_create(cls,lat,long):
        coords = Coordenadas.query.filter((Coordenadas.lat==lat[:8])&(Coordenadas.long==long[:8])).first()
        print(coords)
        if not coords:
            coords = Coordenadas(lat=lat,long=long)
            Coordenadas.add_coords(coords=coords)
        return coords

    __tablename__ = 'coordenadas'
    id = Column(Integer, primary_key=True)
    lat = Column(String(255))
    long = Column(String(255))

    def __init__(self,lat,long):
        self.lat = round(lat,8)
        self.long = round(long,8)


    def assign_constraint(self,constraint):
        self.constraint.append(constraint)

    
    def get_by_id(id):
        return Coordenadas.query.filter(Coordenadas.id==id).first()

    def assign_zonas_inundables(self,zona,coords):
        Coordenadas.add_coords(coords)
        self.zonasInundables.append(zona)
        Coordenadas.update_coords()

    def assign_recorridos_evacuacion(self, recorrido, coords):
        Coordenadas.add_coords(coords)
        self.recorridosEvacuacion.append(recorrido)
        Coordenadas.update_coords()
        
    def delete(self):
        db.session.delete(self)
    

