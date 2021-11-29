from wtforms import (
    Form,
    StringField,
    PasswordField,
    validators,
    SelectMultipleField,
    widgets,
)
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm


class EditZonaInundableForm(FlaskForm):
    """
    Formulario para editar una zona inundable

    Args:
        id = Int id de la zona inundable
        state = Estado de la zona inundable
        color = Color de la zona inundable en el mapa

    """

    id = HiddenField("id")
    name = StringField("Nombre", [validators.DataRequired(message="Campo requerido")])
    state = SelectField("Estado", choices=["Publicado", "Despublicado"])
    color = SelectField(
        "Color",
        choices=[
            ("red", "Rojo"),
            ("blue", "Azul"),
            ("green", "Verde"),
            ("yellow", "Amarillo"),
        ],
    )
