from wtforms import StringField,validators
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm


class CreatePuntoEncuentro(FlaskForm):
    """
    Formulario para registrar un nuevo punto de encuentro

    Args:
        name(string): nombre del punto de encuentro
        address(string): dirección
        email(string): email único del punto de encuentro
        tel(string): teléfono de contacto
        coords(string): coordenadas geográficas del lugar
    """
    name = StringField('Nombre',[validators.DataRequired(message="Campo requerido")])
    address = StringField('Dirección',[validators.DataRequired(message="Campo requerido")])
    email = StringField('Email',[validators.Email(message="Email invalido")])
    tel = StringField('Teléfono',[validators.regexp("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$",message="Numero de telefono inválido")])
    coords = StringField('Coordenadas',[validators.DataRequired(message="Campo requerido")])

class EditPuntoEncuentro(CreatePuntoEncuentro):
    """
    Formulario para editar un punto de encuentro subclase de CreatePuntoEncuentro

    Args:
        id(int): id del punto de encuentro.
    """
    id = HiddenField('Id')

