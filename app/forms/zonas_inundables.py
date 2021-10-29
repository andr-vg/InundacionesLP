from wtforms import Form, StringField, PasswordField, validators, SelectMultipleField, widgets
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm


class EditZonaInundableForm(FlaskForm):
    """
    Formulario para registrar una zona inundable al sistema
    id = Int id de la zona inundable
    state = Estado de la zona inundable
    color = Color de la zona inundable en el mapa

    Args:

    """

    id = HiddenField("id")
    state = BooleanField("Estado", defaults=False)
    color = SelectField("Color",choices=[],[validators.regexp("^#(?:[0-9a-fA-F]{3,4}){1,2}$",message="Se debe ingresar un color valido")])