from wtforms import StringField, validators
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

    name = StringField("Nombre", [validators.DataRequired(message="Campo requerido")])
    address = StringField(
        "Dirección", [validators.DataRequired(message="Campo requerido")]
    )
    email = StringField(
        "Email", [validators.Optional(), validators.Email(message="Email invalido")]
    )
    tel = StringField(
        "Teléfono",
        [
            validators.Optional(),
            validators.regexp(
                "^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$",
                message="Debe ingresar un telefono valido",
            ),
        ],
    )
    lat = StringField("Latitud")
    long = StringField("Longitud")

    def validate_lat(form, field):
        """Se valida la latitud de la denuncia"""
        try:
            if float(field.data) < -90 or float(field.data) > 90:
                raise Exception
        except:
            form.lat.errors = (
                validators.ValidationError(
                    "Se debe ingresar una latitud en un rango -90 a 90"
                ),
            )

    def validate_long(form, field):
        """Se valida la latitud de la denuncia"""
        try:
            if float(field.data) < -180 or float(field.data) > 180:
                raise Exception
        except:
            form.long.errors = (
                validators.ValidationError(
                    "Se debe ingresar una longitud en un rango -180 a 180"
                ),
            )


class EditPuntoEncuentro(CreatePuntoEncuentro):
    """
    Formulario para editar un punto de encuentro subclase de CreatePuntoEncuentro

    Args:
        id(int): id del punto de encuentro.
    """

    id = HiddenField("Id")

    def validate_id(form, field):
        """ " Valida que el input id recibido sea un valor mayor o igual a 1"""

        if int(field.data) < 1:
            form.id.errors = (validators.ValidationError("Formulario invalido"),)
