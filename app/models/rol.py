from app.db import db
from sqlalchemy import Table, ForeignKey, Column, Integer, String, text
from sqlalchemy.orm import relationship
from app.models.permission import Permission


rol_permissions = Table(
    "rol_tiene_permiso",
    db.Model.metadata,
    Column("roles_id", ForeignKey("roles.id"), primary_key=True),
    Column("permisos_id", ForeignKey("permisos.id"), primary_key=True),
)


class Rol(db.Model):
    """ " Modela los roles en el sistema"""

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    users = relationship("User", secondary="usuario_tiene_rol", back_populates="roles")
    permissions = relationship(
        "Permission", secondary=rol_permissions, back_populates="roles"
    )

    def __init__(self, name):
        self.name = name

    def get_all_roles():
        """ " Retorna todos los roles en el sistema"""
        return Rol.query.all()

    def get_rol_by_id(id):
        """ " Retorna el rol que tiene por identificador el id recibido por parametro o None si
        no se encuentra ninguno.
        :params id: Numero entero que representa el identificador del rol."""
        return Rol.query.filter(Rol.id == id).first()

    def get_rol_by_name(name):
        """ " Retorna el rol que tiene por nombre el name recibido por parametro o None si
        no se encuentra ninguno.
        :params name: String que representa el nombre del rol."""
        return Rol.query.filter(Rol.name == name).first()

    def get_permissions(rol_id):
        """ " Retorna los permisos que tiene un Rol determinado por su identificador.
        :params id:Numero entero que representa el identificador del Rol"""
        sql = text(
            "SELECT p.name FROM roles r \
                INNER JOIN rol_tiene_permiso rtp ON (rtp.roles_id = r.id) \
                INNER JOIN permisos p ON (p.id = rtp.permisos_id) \
                WHERE r.id = :rol_id"
        )
        permissions = [elem[0] for elem in db.session.execute(sql, {"rol_id": rol_id})]
        return permissions

    def add_rol(self):
        """Agrega el rol, los cambios no se verán reflejados en la BD hasta
        no hacer un commit"""
        db.session.add(self)
        db.session.commit()
