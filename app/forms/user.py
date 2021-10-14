from wtforms import Form,StringField,PasswordField,validators,SelectMultipleField, widgets
from wtforms.fields.simple import HiddenField
from app.models.rol import Rol



class RegistrationUserForm(Form):
    email = StringField('Email',[validators.DataRequired(message="*"),validators.Email(message="email invalido"),validators.length(min=5,message="Debe tener al menos 5 caracteres")])
    username = StringField('Nombre de usuario', [validators.DataRequired(message="*"),validators.length(min=5,message="Debe tener al menos 5 caracteres")])
    password = PasswordField('Contraseña',[validators.DataRequired(message="*"),validators.EqualTo('confirm',message="Las contraseñas no coinciden")])
    confirm = PasswordField('Confirmar contraseña')
    rol = SelectMultipleField("Seleccionar rol",[validators.DataRequired(message="*")],coerce=int,option_widget = widgets.CheckboxInput()
)
    firstname = StringField('Nombre', [validators.regexp("^[a-zA-Z]+$")])
    lastname = StringField('Apellido', [validators.regexp("^[a-zA-Z]+$")])

class EditUserForm(Form):
    id = HiddenField('Id')
    email = StringField('Email',[validators.DataRequired(message="*"),validators.Email(message="email invalido"),validators.length(min=5,message="Debe tener al menos 5 caracteres")])
    username = StringField('Nombre de usuario', [validators.length(min=5,message="Debe tener al menos 5 caracteres")])
    password = PasswordField('Contraseña',[validators.EqualTo('confirm',message="Las contraseñas no coinciden")])
    confirm = PasswordField('Confirmar contraseña')
    rol = SelectMultipleField("Seleccionar rol",[validators.DataRequired(message="*")],coerce=int,option_widget = widgets.CheckboxInput()
)
    firstname = StringField('Nombre', [validators.regexp("^[a-zA-Z]+$")])
    lastname = StringField('Apellido', [validators.regexp("^[a-zA-Z]+$")])