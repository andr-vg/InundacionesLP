from wtforms import (
    Form,
    StringField,
    PasswordField,
    validators,
    SelectMultipleField,
    widgets,
)
from wtforms.fields.simple import HiddenField
from app.models.rol import Rol
from flask_wtf import FlaskForm


class RegistrationUserForm(FlaskForm):
    """
    Formulario para registrar un usuario al sistema

    Args:
        email(string): email único del usuario
        username(string): nombre único del usuario
        password(string): contraseña
        confirm(string): repetición de contraseña
        rol(list): roles disponibles de un usuario
        firstname(string): nombre del usuario
        lastname(string): apellido del usuario
    """

    email = StringField(
        "Email",
        [
            validators.DataRequired(message="Ingrese un email valido"),
            validators.Email(message="email invalido"),
            validators.length(min=5, message="Debe tener al menos 5 caracteres"),
        ],
    )
    username = StringField(
        "Nombre de usuario",
        [
            validators.DataRequired(message="Ingrese un usuario valido"),
            validators.length(min=5, message="Debe tener al menos 5 caracteres"),
            validators.regexp(
                "^[0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", message="Nombre de usuario inválido"
            ),
        ],
    )
    password = PasswordField(
        "Contraseña",
        [
            validators.DataRequired(message="*"),
            validators.EqualTo("confirm", message="Las contraseñas no coinciden"),
            validators.length(min=4, message="Debe tener al menos 4 caracteres"),
        ],
    )
    confirm = PasswordField("Confirmar contraseña")
    rol = SelectMultipleField(
        "Seleccionar rol",
        [validators.DataRequired(message="Debe seleccionar al menos un rol")],
        coerce=int,
        option_widget=widgets.CheckboxInput(),
    )
    firstname = StringField(
        "Nombre", [validators.regexp("^[a-zA-Z]+$", message="Nombre inválido")]
    )
    lastname = StringField(
        "Apellido", [validators.regexp("^[a-zA-Z]+$", message="Apellido inválido")]
    )


class EditUserForm(RegistrationUserForm):
    """
    Formulario para editar un usuario en el sistema

    Args:
        id(int): id del usuario correspondiente
        email(string): email único del usuario
        username(string): nombre único del usuario
        password(string): contraseña
        confirm(string): repetición de contraseña
        rol(list): roles disponibles de un usuario
        firstname(string): nombre del usuario
        lastname(string): apellido del usuario
    """

    id = HiddenField("Id")
    password = PasswordField(
        "Contraseña",
        [
            validators.EqualTo("confirm", message="Las contraseñas no coinciden"),
            validators.length(min=4, message="Debe tener al menos 4 caracteres"),
        ],
    )
    confirm = PasswordField("Confirmar contraseña")


class EditProfileForm(FlaskForm):
    """
    Formulario para editar el perfil propio

    Args:
        id(int): id del usuario correspondiente
        firstname(string): nombre del usuario
        lastname(string): apellido del usuario
        password(string): contraseña
        confirm(string): repetición de contraseña
    """

    id = HiddenField("Id")
    firstname = StringField(
        "Nombre",
        [validators.regexp("^[a-zA-Z]+$", message="El nombre no puede estar vacío.")],
    )
    lastname = StringField(
        "Apellido",
        [validators.regexp("^[a-zA-Z]+$", message="El apellido no puede estar vacío.")],
    )
    password = PasswordField(
        "Contraseña",
        [
            validators.EqualTo("confirm", message="Las contraseñas no coinciden"),
            validators.length(min=4, message="Debe tener al menos 4 caracteres"),
        ],
    )
    confirm = PasswordField("Confirmar contraseña")
    rol = SelectMultipleField(
        "Seleccionar rol",
        [validators.DataRequired(message="Debe tener al menos un rol")],
        coerce=int,
        option_widget=widgets.CheckboxInput(),
    )
