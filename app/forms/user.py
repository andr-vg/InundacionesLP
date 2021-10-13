from wtforms import Form,StringField,PasswordField,validators,SelectMultipleField, widgets
from app.models.rol import Rol




class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistrationUserForm(Form):
    email = StringField('Email',[validators.DataRequired(),validators.Email(),validators.length(min=5)])
    username = StringField('Nombre de usuario', [validators.DataRequired(),validators.length(min=5)])
    password = PasswordField('Contraseña',[validators.DataRequired(),validators.EqualTo('confirm',message="Las contraseñas no coinciden")])
    confirm = PasswordField('Confirmar contraseña')
    rol = SelectMultipleField("Seleccionar rol",[validators.DataRequired()],coerce=int,option_widget = widgets.CheckboxInput()
)
    firstname = StringField('Nombre', [validators.regexp("^[a-zA-Z]+$")])
    lastname = StringField('Apellido', [validators.regexp("^[a-zA-Z]+$")])

