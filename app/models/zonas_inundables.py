import uuid

from sqlalchemy.orm import relationship
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, text, select, and_,or_


class ZonaInundable(db.Model):
    """
    
    """
    zona_tiene_coords = Table('zona_tiene_coords', db.Model.metadata,
    Column('zonasInundables_id', ForeignKey('zonasInundables.id'), primary_key=True),
    Column('coordenadas_id', ForeignKey('coordenadas.id'), primary_key=True)
)
    @classmethod
    def exists_zona_inundable(cls, name):
        """
        Verifica si ya existe una zona inundable dado un nombre

        Args:
            name: Nombre de la zona inundable que se quiere verificar

        Returns:
            El resultado de la consulta con la zona inundable existente caso contrario None
        """
        zona_inundable = ZonaInundable.query.filter(ZonaInundable.name == name).first()
        return zona_inundable

    __tablename__ = 'zonasInundables'
    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True)
    name = Column(String(255), unique=True)
    state = Column(Boolean, default=False)
    color = Column(String(255), nullable=True)
    coords = relationship('Coordenadas', secondary='zona_tiene_coords', backref='zonasInundables')

    def __init__(self,name,state=True,color="rojo"):
        self.code = self.generate_code()
        self.name = name
        self.state = state
        self.color = color


    def add_zona_inundable(self):
        db.session.add(self)


    def update_zona_inundable(self):
        db.session.commit()


    def generate_code(self):
        return uuid.uuid4()

    def get_zona_by_id(id):
        """ 
        Retorna la zona con el id recibido por parametro 
        """
        return ZonaInundable.query.filter(ZonaInundable.id==id).first()

    def get_index_zonas(page, config):
        """
        Retorna el listado de zonas ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        Args:
            page: Numero entero que representa la pagina.
            config: Representa la configuracion del sistema. 
        """
        if config.ordered_by == "Ascendente":
            return ZonaInundable.query.order_by(ZonaInundable.name.asc()).paginate(page, per_page=config.elements_per_page)
        return ZonaInundable.query.order_by(ZonaInundable.name.desc()).paginate(page, per_page=config.elements_per_page)


    def get_zonas_paginated(page, elements_per_page):
        return ZonaInundable.query.paginate(page, per_page=elements_per_page)