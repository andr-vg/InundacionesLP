from wtforms import Form, StringField, PasswordField, validators, SelectMultipleField, widgets
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm


class CreateSeguimientoForm(FlaskForm):
    """ 
    Formulario del seguimiento
    """
    description = StringField("Descripcion", [validators.DataRequired()],widget=widgets.TextArea())