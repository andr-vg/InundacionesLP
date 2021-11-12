from wtforms import Form, StringField, PasswordField, validators, SelectMultipleField, widgets
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm, csrf
from app.models.categories import Categoria
from app.models.user import User


class CreateDenunciaForm(FlaskForm):
    """"
    
    """
    title = StringField("Titulo",[validators.DataRequired(message="Debe ingresar un titulo")])
    category = SelectField("Categoria",coerce=int)
    description = StringField("Descripcion", [validators.DataRequired("Debe ingresar una descripcion"),
    validators.Length(min=1,max=255,message="No puede superar los 255 caracteres")],widget=widgets.TextArea())
    lat = StringField("Latitud")
    long = StringField("Longitud")
    firstname = StringField("Nombre",[validators.DataRequired(message="Debe ingresar su nombre"),
    validators.regexp("^[a-zA-Z]+$",message="Debe ingresar un nombre valido")])
    lastname = StringField("Apellido",[validators.DataRequired(message="Debe ingresar su apellido"),
    validators.regexp("^[a-zA-Z]+$",message="Debe ingresar un apellido valido")])
    tel = StringField("Teléfono",[validators.regexp("^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$",
    message="Debe ingresar un telefono valido"),validators.DataRequired(message="Debe ingresar un teléfono valido")])
    email = StringField("Email", [validators.DataRequired(message="Debe ingresar un email"),
    validators.Email(message="Debe ingresar un email valido")])
    user = SelectField("Usuario asignado",coerce=int)


    def __init__(self,*args,**kwargs):
        super().__init__(*args)
        self.category.choices = [(0,"Sin asignar")]+[(category.id,category.name) for category in Categoria.get_all()]
        self.user.choices = [(0,"Sin asignar")]+[(user.id,user.email) for user in User.get_with_state(User.get_all(),True)]
        if kwargs:
            self.title.data = kwargs["title"]
            self.description.data = kwargs["description"]
            self.lat.data = kwargs["lat"]
            self.long.data = kwargs["long"]
            self.firstname.data = kwargs["firstname"]
            self.lastname.data = kwargs["lastname"]
            self.tel.data = kwargs["tel"]
            self.email.data = kwargs["email"]
            if not "user" in kwargs.keys() or kwargs["user"]==None:
                self.user.data = 0
            else:
                self.user.data = int(kwargs["user"])
            if not "category" in kwargs.keys() or kwargs["category"]==None:
                self.category.data = 0
            else:
                self.category.data = int(kwargs["category"])
    

    def validate_user(form,field):
        choices = dict(form.user.choices).keys()
        if not (field.data in choices):
            form.user.errors = (validators.ValidationError("Usuario invalido, elija un usuario cargado en el sistema"),)

    
    def validate_category(form,field):
        choices = dict(form.category.choices).keys()
        if not (field.data in choices):
            form.user.errors = (validators.ValidationError("Usuario invalido, elija una categoria valida"),)

    
        

