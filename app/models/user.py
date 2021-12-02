import re
import bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime

from sqlalchemy.sql.expression import false
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
from sqlalchemy.orm import relationship
from app.models.rol import Rol
from app.models.denuncias import Denuncia
from app.models.seguimiento import Seguimiento


user_roles = Table(
    "usuario_tiene_rol",
    db.Model.metadata,
    Column("usuarios_id", ForeignKey("usuarios.id"), primary_key=True),
    Column("roles_id", ForeignKey("roles.id"), primary_key=True),
)


class User(db.Model):
    """
    Clase Usuario para el modelado de la tabla usuarios en el sistema

    Args:
        id(int): id del usuario
        firstname(string): nombre del usuario
        lastname(string): apellido del usuario
        username(string): nombre único del usuario
        email(string): email único del usuario
        password_hash(string): contraseña
        confirm(string): repetición de contraseña
        roles(list): roles disponibles de un usuario
        active(bool): estado activo del usuario
        deleted(bool): estado borrado del usuario
        updated_at(DateTime): momento en el que fue editado
        created_at(DateTime): momento en el que fue creado
    """

    @classmethod
    def login(cls, params):
        """
        Verifica si un usuario puede iniciar sesión en el sistema

        Args:
            params(dict): contiene los parámetros email y password
                          de inicio de sesión
        Returns:
            resultado de la query con el usuario
        """
        user = User.query.filter(User.email == params["email"]).first()
        if (
            user
            and not user.deleted
            and user.active
            and user.verify_password(params["password"])
        ):
            return user
        return None

    @classmethod
    def get_permissions(cls, user_id):
        """
        Obtiene los permisos de un usuario

        Args:
            user_id(int): id del usuario
        Returns:
            list: listado con los permisos del usuario
        """
        sql = text(
            "SELECT p.name \
                FROM usuarios u  \
                INNER JOIN usuario_tiene_rol utr ON(utr.usuarios_id = u.id) \
                INNER JOIN roles r ON(r.id = utr.roles_id) \
                INNER JOIN rol_tiene_permiso rtp ON (rtp.roles_id = r.id) \
                INNER JOIN permisos p ON (p.id = rtp.permisos_id) \
                WHERE u.id = :user_id"
        )
        permissions = [
            elem[0] for elem in db.session.execute(sql, {"user_id": user_id})
        ]
        return permissions

    @classmethod
    def has_permission(cls, user_id, permission):
        """
        Verifica si un usuario posee un dado permiso

        Args:
            user_id(int): id del usuario
            permission(string): permiso

        Returns:
            bool: True or False
        """
        return permission in User.get_permissions(user_id)

    @classmethod
    def get_id_from_email(cls, user_email):
        """
        Obtiene el id (si existe) de un usuario

        Args:
            user_email(string): email del usuario

        Returns:
            int: id del usuario caso contrario None
        """
        sql = text(
            "SELECT id \
                    FROM usuarios \
                    WHERE email = :user_email"
        )
        id = list(db.session.execute(sql, {"user_email": user_email}))
        return id[0][0]

    @classmethod
    def exists_user(cls, username, email):
        """
        Verifica si ya existe un usuario con un dado email y username

        Args:
            username(string): nombre de usuario a comprobar
            email(String): email a comprobar

        Returns:
            El resultado de la consulta con el usuario existente caso contrario None
        """
        user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        return user

    @classmethod
    def exists_user_with_username(cls, username):
        """
        Verifica si un usuario con un dado username ya existe en el sistema

        Args:
            username(string): nombre del usuario

        Returns: primer resultado encontrado en la tabla caso contrario None
        """
        return User.query.filter(User.username == username).first()

    @classmethod
    def exists_user_with_email(cls, email):
        """
        Verifica si un usuario con un dado email ya existe en el sistema

        Args:
            email(string): email del usuario

        Returns: primer resultado encontrado en la tabla caso contrario None
        """
        return User.query.filter(User.email == email).first()

    @classmethod
    def search_by_name(cls, username):
        """
        Busca un usuario con un nombre de usuario similar al parametro

        Args:
            username(string): nombre del usuario

        Returns: primer resultado encontrado en la tabla caso contrario None
        """
        return User.query.filter(User.username.like("%" + username + "%"))

    @classmethod
    def get_with_state(cls, query, state):
        """
        Retorna los usuarios que poseen estado activo o inactivo

        Args:
            query(Query): usuarios a filtrar
            state(bool): estado
        """
        return query.filter(User.active == state)

    @classmethod
    def search_paginate(cls, query, id, page, config):
        """
        Busca usuarios respetando la configuracion y los retorna paginadamente

        Args:
            query(Query): usuarios a filtrar
            id(int): id del usuario en la sesión actual
            page(int): número de página
            config(dict): diccionario con los datos de configuracion a respetar

        """
        if config.ordered_by == "Ascendente":
            return (
                query.filter(User.deleted == False)
                .filter(User.id != id)
                .order_by(User.username.asc())
                .paginate(page, per_page=config.elements_per_page)
            )
        return (
            query.filter(User.deleted == False)
            .filter(User.id != id)
            .order_by(User.username.desc())
            .paginate(page, per_page=config.elements_per_page)
        )

    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(128))
    roles = relationship("Rol", secondary="usuario_tiene_rol", back_populates="users")
    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    pending = Column(Boolean, default=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow, default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    complaints = relationship("Denuncia", back_populates="user_assign")
    tracking = relationship("Seguimiento", back_populates="user_assign")

    def __init__(
        self, email, username, password=None, roles=None, firstname=None, lastname=None
        , pending=False
    ):
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password).decode("utf-8")
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.pending = pending

    @property
    def password(self):
        """
        Levanta una excepción que no permite leer la contraseña
        """
        raise AttributeError("La contraseña no es un atributo legible.")

    @password.setter
    def password(self, password):
        """
        Genera el hash para la contraseña ingresada por parámetro

        Args:
            password(string): contraseña ingresada
        """
        self.password_hash = generate_password_hash(password)

    def edit_profile(self, form, roles_deleted):
        """Edita el perfil del usuario actual"""
        if form.password.data:
            self.password = form.password.data
        self.firstname = form.firstname.data
        self.lastname = form.lastname.data
        for rol in roles_deleted:
            rol_deleted = Rol.get_rol_by_id(rol)
            self.roles.remove(rol_deleted)
        for rol in form.rol.data:
            rol_new = Rol.get_rol_by_id(rol)
            self.roles.append(rol_new)
        db.session.commit()

    def change_state(self):
        """
        Invierte el estado de un usuario
        """
        self.active = not self.active
        db.session.commit()

    def add_user(self):
        """Agrega el usuario, los cambios no se verán reflejados en la BD hasta
        no hacer un commit"""
        db.session.add(self)
        db.session.commit()

    def edit_user(self, form, roles_deleted):
        """Editar a un usuario y sus roles"""
        self.username = form.username.data
        self.email = form.email.data
        if form.password.data:
            self.password = form.password.data
        self.firstname = form.firstname.data
        self.lastname = form.lastname.data
        for rol in roles_deleted:
            rol_deleted = Rol.get_rol_by_id(rol)
            self.roles.remove(rol_deleted)
        for rol in form.rol.data:
            rol_new = Rol.get_rol_by_id(rol)
            self.roles.append(rol_new)
        db.session.commit()

    def add_rol(self, rol):
        self.roles.append(rol)
        db.session.commit()

    def activate(self):
        self.deleted = False
        db.session.commit()

    def delete(self):
        self.deleted = True
        for complaint in self.complaints:
            complaint.disassign_user()
        db.session.commit()

    def assign_complaints(self, complaint):
        """Asigna la denuncia a la relacion"""
        self.complaints.append(complaint)
        db.session.commit()

    def assign_tracking(self, tracking):
        """Asigna el seguimiento a la relacion"""
        self.tracking.append(tracking)
        db.session.commit()

    def verify_password(self, password):
        """
        Verifica si la contraseña por parámetro coincide
        con la existente encriptada.

        Args:
            password(string): contraseña a filtrar
        """
        return check_password_hash(self.password_hash, password)

    def get_user_by_id(id):
        """
        Retorna el primer usuario con un dado id

        Args:
            id(int): id a filtrar
        """
        return User.query.filter(User.id == id).first()

    def get_user_by_email(email):
        """
        Retorna el primer usuario con un dado email

        Args:
            email(string): email a filtrar
        """
        return User.query.filter(User.email == email).first()

    def get_user_by_username(username):
        """
        Retorna el primer usuario con un dado username

        Args:
            username(string): nombre de usuario a filtrar
        """
        return User.query.filter(User.username == username).first()

    def get_all():
        """Retorna el listado de todos los usuarios no eliminados"""
        return User.query.filter((User.deleted == False) & (User.active == True))

    def get_index_users(id, page, config):
        """
        Retorna los usuarios de manera paginada según la configuracion dada

        Args:
            id(int): id del usuario activo en la sesión
            page(int): número a paginar
            config(dict): diccionario con los datos de configuracion establecidos
        """
        if config.ordered_by == "ascendente":
            return (
                User.query.filter(User.deleted == False)
                .filter(User.id != id)
                .order_by(User.username.asc())
                .paginate(page, per_page=config.elements_per_page)
            )
        return (
            User.query.filter(User.deleted == False)
            .filter(User.id != id)
            .order_by(User.username.desc())
            .paginate(page, per_page=config.elements_per_page)
        )
