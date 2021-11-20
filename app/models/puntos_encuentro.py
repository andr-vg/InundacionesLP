import datetime


from app.db import db
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import relationship


class PuntosDeEncuentro(db.Model):
    """ " Modelo de Puntos de encuentro"""

    @classmethod
    def get_all(cls):
        """ " Retorna la consulta de todos los puntos de encuentro en la base de datos"""
        return PuntosDeEncuentro.query.all()

    @classmethod
    def get_all_publish(cls):
        """Retorna la consulta de todos los puntos de encuentro publicados"""
        return PuntosDeEncuentro.query.filter(PuntosDeEncuentro.state == False)

    @classmethod
    def search_by_name(cls, name):
        """ " Retorna la consulta de los puntos de encuentro que contienen el nombre recibido por parametro
        :param name:Cadena de string a buscar en los nombres de los puntos de encuentro.
        """
        return PuntosDeEncuentro.query.filter(
            PuntosDeEncuentro.name.like("%" + name + "%")
        )

    @classmethod
    def filter_by_state(cls, query, state):
        """ " Filtra los puntos de encuentro por estado.
        :params: query: Consulta previa en la base de datos.
        :params: state: String que representa el estado del punto de encuentro."""
        if state == "activo":
            return query.filter(PuntosDeEncuentro.state == True)
        return query.filter(PuntosDeEncuentro.state == False)

    @classmethod
    def unique_fields(cls, name, address):
        """ " Retorna los puntos de encuentro con el nombre o la direccion pasada por parametro.
        :params name: String que representa el nombre del punto de encuentro.
        :params address: String que representa la direccion del punto de encuentro."""
        punto_encuentro = PuntosDeEncuentro.query.filter(
            (PuntosDeEncuentro.name == name) | (PuntosDeEncuentro.address == address)
        ).first()
        return punto_encuentro

    @classmethod
    def search_paginate(cls, query, page, config):
        """
        Busca puntos de encuentro respetando la configuracion y los retorna paginadamente

        Args:
            query(Query): puntos de encuentro a filtrar
            page(int): número de página
            config(dict): diccionario con los datos de configuracion a respetar

        """
        if config.ordered_by == "ascendente":
            return query.order_by(PuntosDeEncuentro.name.asc()).paginate(
                page, per_page=config.elements_per_page
            )
        return query.order_by(PuntosDeEncuentro.name.desc()).paginate(
            page, per_page=config.elements_per_page
        )

    __tablename__ = "puntosEncuentro"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    address = Column(String(255), unique=True)
    tel = Column(String(255))
    email = Column(String(255))
    state = Column(Boolean, default=False)
    lat = Column(Float)
    long = Column(Float)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, address, tel, email, lat, long):
        self.email = email
        self.address = address
        self.name = name
        self.tel = tel
        self.lat = lat
        self.long = long

    def edit(self, name, address, tel, email, lat, long):
        self.email = email
        self.address = address
        self.name = name
        self.tel = tel
        self.lat = lat
        self.long = long
        db.session.commit()

    def add_punto_encuentro(self):
        """Agrega el punto de encuentro, los cambios no se verán reflejados en la BD hasta
        no hacer un commit"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def change_state(self):
        self.state = not self.state
        db.session.commit()

    def get_punto_by_id(id):
        """ " Retorna el punto de encuentro con el id ingresado por parametro o None si no
        se encuentra ninguno con dicho id.
        :params id:Numero entero que representa el identificador del punto de encuentro."""
        return PuntosDeEncuentro.query.filter(PuntosDeEncuentro.id == id).first()

    def get_punto_by_name(name):
        """ " Retorna el punto de encuentro con el name ingresado por parametro o None
        si no se encuentra ninguno con dicho nombre .
           :params name:String que representa el nombre del punto de encuentro."""
        return PuntosDeEncuentro.query.filter(
            PuntosDeEncuentro.name == name.upper()
        ).first()

    def get_punto_by_address(address):
        """ " Retorna el punto de encuentro con el address ingresado por parametro o None si no se encuentra
        ninguno con dicha dirección .
        :params address:String que representa la direccion del punto de encuentro."""
        return PuntosDeEncuentro.query.filter(
            PuntosDeEncuentro.address == address.upper()
        ).first()

    def get_index_puntos_encuentro(page, config):
        """ " Retorna el listado de puntos de encuentro ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        :param page:Numero entero que representa la pagina.
        :param config: Representa la configuracion del sistema."""
        if config.ordered_by == "ascendente":
            return PuntosDeEncuentro.query.order_by(
                PuntosDeEncuentro.name.asc()
            ).paginate(page, per_page=config.elements_per_page)
        return PuntosDeEncuentro.query.order_by(PuntosDeEncuentro.name.desc()).paginate(
            page, per_page=config.elements_per_page
        )
