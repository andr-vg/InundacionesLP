from wtforms import Form, StringField, PasswordField, validators, SelectMultipleField, widgets
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm
from app.models.denuncias import State


class CreateSeguimientoForm(FlaskForm):
    """ 
    """
    description = StringField("Descripcion", [validators.DataRequired()],widget=widgets.TextArea())
    state = SelectField("Estado",choices=State.choices())