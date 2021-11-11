import datetime
from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

import app.models.coordenadas as c


class Recorridos(db.Model):
    """
    Modelo que define los recorridos de evacuación.

    Args:
        name (string): nombre del recorrido de evacuación
        description (string): descripción del mismo
        state (boolean): estado (0 despublicado, 1 publicado)
        
    """
    @classmethod
    def unique_field(cls, name):
        """
        Verifica si ya existe un recorrido con el nombre recibido por parametro

        Args:
            name: String
        Returns:
            El resultado de la consulta con recorrido existente caso contrario None
        """
        recorrido = Recorridos.query.filter(Recorridos.name == name).first()
        return recorrido

    @classmethod
    def get_all(cls):
        """ 
        Retorna la consulta de todos los recorridos de evacuacion
        en la base de datos 
        """
        return Recorridos.query.all()

    @classmethod
    def search_by_name(cls, name):
        """
        Busca un recorrido con un nombre similar al pasado por parametro

        Args: 
            name(string): nombre del recorrido

        Returns: primer resultado encontrado en la tabla caso contrario None
        """
        return Recorridos.query.filter(Recorridos.name.like('%'+name+'%'))
    
    @classmethod
    def get_with_state(cls, query, state):
        """
        Retorna los recorridos que poseen estado activo o inactivo

        Args: 
            query(Query): recorridos a filtrar
            state(bool): estado 
        """
        return query.filter(Recorridos.active==state)

    @classmethod
    def search_paginate(cls, query, page, config):
        """
        Busca recorridos respetando la configuracion y los retorna paginadamente

        Args:
            query(Query): recorridos a filtrar
            page(int): número de página 
            config(dict): diccionario con los datos de configuracion a respetar

        """
        if config.ordered_by == "Ascendente":
            return query.order_by(Recorridos.name.asc()).paginate(page, per_page=config.elements_per_page)
        return query.order_by(Recorridos.name.desc()).paginate(page, per_page=config.elements_per_page)

    recorrido_tiene_coords = Table('recorrido_tiene_coords', db.Model.metadata,
        Column('recorridosEvacuacion_id', ForeignKey('recorridosEvacuacion.id'), primary_key=True),
        Column('coordenadas_id', ForeignKey('coordenadas.id'), primary_key=True))

    __tablename__ = "recorridosEvacuacion"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255), unique=True)
    state = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    coords = relationship('Coordenadas', secondary='recorrido_tiene_coords', backref='recorridosEvacuacion')


    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def edit(self, name, description):
        self.name = name
        self.description = description
        for elem in self.coords:
            coordinate = c.Coordenadas.get_by_id(elem.id)
            coordinate.delete()
        
        

    def add_coordinate(self, new_coords):
        self.coords.append(new_coords)

    def add_recorrido(self):
        """ 
        Agrega el recorrido de evacuación, los cambios no se verán reflejados en la BD hasta 
        no hacer un commit 
        """
        db.session.add(self)

    def update(self):
        """ 
        Actualiza el modelo en la BD 
        """
        db.session.commit()

    def delete(self):
        for elem in self.coords:
            coordinate = c.Coordenadas.get_by_id(elem.id)
            coordinate.delete()
        db.session.delete(self)

    def change_state(self):
        self.state = not self.state

    def get_recorrido_by_id(id):
        """ 
        Retorna el recorrido de evacuación con el id ingresado por parametro 
        o None si no se encuentra ninguno con dicho id.
        :params id: Numero entero que representa el identificador del recorrido. 
        """
        return Recorridos.query.filter(Recorridos.id==id).first()
    
    def get_recorrido_by_name(name):
        """
        Retorna el recorrido con el name ingresado por parametro o None
        si no se encuentra ninguno con dicho nombre.
        :params name:String que representa el nombre del punto de encuentro. 
        """
        return Recorridos.query.filter(Recorridos.name==name.upper()).first()

    def get_index_recorridos(page, config):
        """
        Retorna el listado de recorridos ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        :param page: Numero entero que representa la pagina.
        :param config: Representa la configuracion del sistema. """
        if config.ordered_by == "Ascendente":
            return Recorridos.query.order_by(Recorridos.name.asc()).paginate(page, per_page=config.elements_per_page)
        return Recorridos.query.order_by(Recorridos.name.desc()).paginate(page, per_page=config.elements_per_page)    