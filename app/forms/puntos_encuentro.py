from sqlalchemy.sql.sqltypes import String
from wtforms import Form,StringField,PasswordField,validators,SelectMultipleField, widgets
from wtforms.fields.simple import HiddenField

class CreatePuntoEncuentro(Form):
    """
    Formulario para registrar un nuevo punto de encuentro

    Args:
        name(string): nombre del punto de encuentro
        address(string): dirección
        email(string): email único del punto de encuentro
        tel(string): teléfono de contacto
        coords(string): coordenadas geográficas del lugar
    """
    name = StringField('Nombre',[validators.DataRequired(message="*")])
    address = StringField('Dirección',[validators.DataRequired(message="*")])
    email = StringField('Email',[validators.Email(message="Email invalido")])
    tel = StringField('Teléfono',[validators.regexp("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$",message="Numero de telefono inválido")])
    coords = StringField('Coordenadas',[validators.DataRequired()])

class EditPuntoEncuentro(CreatePuntoEncuentro):
    """
    Formulario para editar un punto de encuentro subclase de CreatePuntoEncuentro

    Args:
        id(int): id del punto de encuentro.
    """
    id = HiddenField('Id')

