import uuid

from sqlalchemy.orm import relationship
from app.db import db
from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    text,
    select,
    and_,
    or_,
)
from app.helpers.colors import get_translated_color


class ZonaInundable(db.Model):
    """
    Modelo que define las zonas inundables.

    Args:
        name (string): nombre de la zona inundable
        code (string): Codigo unico de la zona
        state (boolean): estado (0 despublicado, 1 publicado)
        color(string): Color con el que se representara la zona en el mapa
        coords(Coordenadas): Coordenadas asociadas a la zona inundable
    """

    @classmethod
    def get_all(cls):
        """
        Devuelve todas las zonas inundables de la BD
        """
        return ZonaInundable.query.all()

    @classmethod
    def get_all_publicated(cls, config):
        """
        Devuelve todas las zonas inundables de la BD

        Args:
            config(dict): contiene los datos de configuracion actuales
        """
        if config.ordered_by == "ascendente":
            return ZonaInundable.query.filter(ZonaInundable.state == 1).order_by(
                ZonaInundable.name.asc()
            )
        return ZonaInundable.query.filter(ZonaInundable.state == 1).order_by(
            ZonaInundable.name.desc()
        )

    zona_tiene_coords = Table(
        "zona_tiene_coords",
        db.Model.metadata,
        Column(
            "zonasInundables_id", ForeignKey("zonasInundables.id"), primary_key=True
        ),
        Column("coordenadas_id", ForeignKey("coordenadas.id"), primary_key=True),
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

    @classmethod
    def search_by_name(cls, name):
        """
        Busca una zona inundable con nombre similar al parametro

        Args:
            name(string): nombre de la zona inundable

        Returns: primer resultado encontrado en la tabla caso contrario None
        """
        return ZonaInundable.query.filter(ZonaInundable.name.like("%" + name + "%"))

    @classmethod
    def get_with_state(cls, query, state):
        """
        Retorna los zonas que poseen estado activo o inactivo

        Args:
            query(Query): zona a filtrar
            state(bool): estado
        """
        return query.filter(ZonaInundable.state == state)

    @classmethod
    def search_paginate(cls, query, page, config):
        """
        Busca zonas indundables respetando la configuracion y los retorna paginadamente

        Args:
            query(Query): zonas a filtrar
            page(int): número de página
            config(dict): diccionario con los datos de configuracion a respetar

        """
        if config.ordered_by == "ascendente":
            return query.order_by(ZonaInundable.name.asc()).paginate(
                page, per_page=config.elements_per_page
            )
        return query.order_by(ZonaInundable.name.desc()).paginate(
            page, per_page=config.elements_per_page
        )

    __tablename__ = "zonasInundables"
    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True)
    name = Column(String(255), unique=True)
    state = Column(Boolean, default=False)
    color = Column(String(255), nullable=True)
    coords = relationship(
        "Coordenadas", secondary="zona_tiene_coords", backref="zonasInundables"
    )

    def __init__(self, name, state=True, color="rojo"):
        self.code = self.generate_code()
        self.name = name
        self.state = state
        self.color = color

    def edit(self, name, state=True, color="rojo"):
        self.name = name
        self.state = state
        self.color = color
        db.session.commit()

    def add_zona_inundable(self):
        """
        Agrega una zona, los cambios no se verán reflejados en la BD hasta
        no hacer un commit
        """
        db.session.add(self)
        db.session.commit()

    def generate_code(self):
        """
        Genera un codigo unico, el cual se usara como codigo a la hora de agregar una zona
        """
        return uuid.uuid4()

    def get_zona_by_id(id):
        """
        Retorna la zona con el id recibido por parametro
        """
        return ZonaInundable.query.filter(ZonaInundable.id == id).first()

    def get_zona_by_name(name):
        """
        Retorna la zona con el nombre recibido por parametro
        """
        return ZonaInundable.query.filter(ZonaInundable.name == name).first()

    def get_index_zonas(page, config):
        """
        Retorna el listado de zonas ordenado con la configuracion del sistema y paginado con
        la cantidad de elementos por pagina definidos en la configuracion del sistema.
        Args:
            page: Numero entero que representa la pagina.
            config: Representa la configuracion del sistema.
        """
        if config.ordered_by == "ascendente":
            return ZonaInundable.query.order_by(ZonaInundable.name.asc()).paginate(
                page, per_page=config.elements_per_page
            )
        return ZonaInundable.query.order_by(ZonaInundable.name.desc()).paginate(
            page, per_page=config.elements_per_page
        )

    def get_zonas_paginated(page, config):
        """
        Devuelve todas las zonas publicadas paginadas, se utilizara en la api
        Args:
            page(int): Numero entero que representa la pagina
            config(dict): configuracion actual del sistema
        """
        return ZonaInundable.get_all_publicated(config).paginate(
            page, per_page=int(config.elements_per_page)
        )

    def get_coords_as_list(self):
        """
        Devuelve las coordenadas asociadas a la zona, en forma de lista
        """
        lista = []
        for c in self.coords:
            lista.append([c.lat, c.long])
        return lista

    def get_coords_lenght(self):
        """
        Devuelve la cantidad de coordenadas asociadas a la zona
        """
        return len(self.coords)

    def get_color(self):
        """
        Devuelve el nombre del color, traducido al ingles, para poder usarlo  a la hora
        de marcar los puntos dela zona en el mapa.
        """
        return get_translated_color(self.color)

    def delete(self):
        """
        Elimina una zona inundable
        """
        db.session.delete(self)
        db.session.commit()

    def change_state(self):
        """
        Cambia el estado de la zona inundable
        """
        self.state = not self.state
        db.session.commit()
