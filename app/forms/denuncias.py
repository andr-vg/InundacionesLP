from sqlalchemy.sql.base import Executable
from wtforms import Form, StringField, PasswordField, validators, SelectMultipleField, widgets
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm, csrf
from app.models.categories import Categoria
from app.models.user import User
from app.models.denuncias import State


class CreateDenunciaForm(FlaskForm):
    """"
    Formulario para las denuncias

    Args:
        title(string): título de la denuncia
        category(int): categoria de la misma
        description(string): descripción de la misma
        lat(string): coordenada latitud
        long(string): coordenada longitud
        firstname(string): nombre del denunciante
        lastname(string): apellido del denunciante
        tel(string): telefono del denunciante
        email(string): mail del denunciante
        user(Usuario): usuario asignado a seguir la denuncia 
    """
    title = StringField("Titulo",[validators.DataRequired(message="Debe ingresar un titulo")])
    category = SelectField("Categoria",[validators.DataRequired(message="Debe seleccionarse una categoria")],coerce=int)
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
        """
        Se valida el usuario elegido para seguir la denuncia
        """
        choices = dict(form.user.choices).keys()
        if not (field.data in choices):
            form.user.errors = (validators.ValidationError("Usuario invalido, elija un usuario cargado en el sistema"),)

    
    def validate_category(form,field):
        """
        Se valida la categoría de la denuncia
        """
        choices = dict(form.category.choices).keys()
        if field.data==0:
            form.category.errors = (validators.ValidationError("Categoría inválida, elija una categoria valida"),)
        if not (field.data in choices):
            form.category.errors = (validators.ValidationError("Categoría inválida, elija una categoria valida"),)

    
    def validate_lat(form,field):
        """ Se valida la latitud de la denuncia"""
        try:
            if float(field.data)<-90 or float(field.data)>90:
                raise Exception
        except:
            form.lat.errors = (validators.ValidationError("Se debe ingresar una latitud en un rango -90 a 90"),)


    def validate_long(form,field):
        """ Se valida la latitud de la denuncia"""
        try:
            if float(field.data)<-180 or float(field.data)>180:
                raise Exception
        except:
            form.long.errors = (validators.ValidationError("Se debe ingresar una longitud en un rango -180 a 180"),)



class EditDenunciaForm(CreateDenunciaForm):
    """"
    Formulario para las denuncias

    Args:
        state(list): título de la denuncia
    """
    state = SelectField("Estado",choices=State.choices())


    def validate_state(form,field):
        """ 
        Se valida el estado de la denuncia
        """
        choices = dict(form.state.choices).keys()
        if not(field.data in choices):
            form.category.errors = (validators.ValidationError("Estado inválido, elija un estado valida"),)