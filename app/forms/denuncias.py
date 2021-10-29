from sqlalchemy.sql.sqltypes import String
from wtforms import Form, StringField, PasswordField, validators, SelectMultipleField, widgets
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm


class CreateDenunciaForm(FlaskForm):
    """"
    
    """

    title = StringField("Titulo",[validators.DataRequired(message="Debe ingresar un titulo")])
    category = SelectField("Categoria", choices=["Cloacas","Acumulacion de basura"])
    description = StringField("Descripcion", [validators.DataRequired()])
    lat = StringField("Latitud")
    long = StringField("Longitud")
    firstname = StringField("Nombre",[validators.DataRequired("Debe ingresar su nombre"),
    validators.regexp("^[a-zA-Z]+$",message="Debe ingresar un nombre valido")])
    lastname = StringField("Apellido",[validators.DataRequired("Debe ingresar su apellido"),
    validators.regexp("^[a-zA-Z]+$",message="Debe ingresar un apellido valido")])
    tel = StringField("Teléfono",[validators.DataRequired("Debe ingresar un teléfono ")])
    email = StringField("Email", [validators.DataRequired("Debe ingresar un email"),
    validators.Email("Debe ingresar un email valido")])
