from wtforms import Form, StringField, PasswordField, validators, SelectMultipleField, widgets
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm
from app.models.categories import Categoria
from app.models.user import User


class CreateDenunciaForm(FlaskForm):
    """"
    
    """

    title = StringField("Titulo",[validators.DataRequired(message="Debe ingresar un titulo")])
    category = SelectField("Categoria",coerce=int)
    description = StringField("Descripcion", [validators.DataRequired()],widget=widgets.TextArea())
    lat = StringField("Latitud")
    long = StringField("Longitud")
    firstname = StringField("Nombre",[validators.DataRequired("Debe ingresar su nombre"),
    validators.regexp("^[a-zA-Z]+$",message="Debe ingresar un nombre valido")])
    lastname = StringField("Apellido",[validators.DataRequired("Debe ingresar su apellido"),
    validators.regexp("^[a-zA-Z]+$",message="Debe ingresar un apellido valido")])
    tel = StringField("Teléfono",[validators.DataRequired("Debe ingresar un teléfono ")])
    email = StringField("Email", [validators.DataRequired("Debe ingresar un email"),
    validators.Email("Debe ingresar un email valido")])
    user = SelectField("Usuario asignado",coerce=int)


    def __init__(self,*args,**kwargs):
        super().__init__(*args)
        self.title.data = kwargs["title"]
        self.description.data = kwargs["description"]
        self.lat.data = kwargs["lat"]
        self.long.data = kwargs["long"]
        self.firstname.data = kwargs["firstname"]
        self.lastname.data = kwargs["lastname"]
        self.tel.data = kwargs["tel"]
        self.email.data = kwargs["email"]
        self.category.choices = [(0,"")]+[(category.id,category.name) for category in Categoria.get_all()]
        self.user.choices = [(0,"")]+[(user.id,user.email) for user in User.get_with_state(User.get_all(),True)]
        if not kwargs["user"]:
            self.user.data = 0
        else:
            self.user.data = int(kwargs["user"])
        if not kwargs["category"]:
            self.category.data = 0
        else:
            self.category.data = int(kwargs["category"])
        
        