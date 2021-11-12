from wtforms import StringField,validators
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm
from wtforms.widgets import TextArea


class CreateRecorrido(FlaskForm):
    """
    Formulario para registrar un nuevo recorrido

    Args:
        name(string): nombre del recorrido (unico)
        description(string): descripcion del recorrido
        coordenadas(string): coordenadas del lugar
    """
    name = StringField('Nombre',[validators.DataRequired(message="Campo requerido"), 
        validators.length(min=4,message="Debe tener al menos 4 caracteres"),
        validators.length(max=250,message="No puede excederse de 250 caracteres"),
        validators.regexp("^[0-9]*[a-zA-Z]+[a-zA-Z0-9]*$",message="Nombre ingresado inválido")])
    description = StringField('Descripcion', [validators.length(max=250,message="No puede excederse de 250 caracteres")], widget=TextArea())
    coordinates = HiddenField('Coordinates')

class EditRecorrido(CreateRecorrido):
    """
    Formulario para editar un recorrido subclase de CreateRecorrido

    Args:
        id(int): id del recorrido
    """
    id = HiddenField('Id')

    def validate_id(form, field):
        """
        Valida que el input id recibido sea un numero mayor o igual a 1 
        """
        
        if int(field.data) < 1:
            form.id.errors = (validators.ValidationError("Formulario invalido"),)