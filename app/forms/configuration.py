from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField
from wtforms.fields.core import SelectField
    
    
    
class ConfigurationForm(FlaskForm):
    """
    Formulario para actualizar la configuracion

    Args:
        elements_per_page(int): cantidad de elementos por pagina
        ordered_by(string): String que indica el orden de los listados
        css_private(string): String que indica el CSS a utilizar en el sitio privado
        css_public(string): String que indica el CSS a utilizar en el sitio público
    """

    elements_per_page = StringField("Elementos por página",[validators.DataRequired(message="Se requiere ingresar un numero de 1 a 20")])
    ordered_by = SelectField("Ordenado por")
    css_private = SelectField("CSS Privado")
    css_public = SelectField("CSS Público")

    def __init__(self,*args,**kwargs):
        super().__init__(*args)
        self.elements_per_page.data =kwargs["elements_per_page"]
        self.ordered_by.choices=[("ascendente","Ascendente"),("descendente","Descendente")]
        self.ordered_by.data=kwargs["ordered_by"]
        self.css_private.choices=[("private1.css","Tema Principal"),("private2.css","Tema Oscuro"),("private3.css","Tema Claro")]
        self.css_private.data=kwargs["css_private"]
        self.css_public.choices=[("private1.css","Tema Principal"),("private2.css","Tema Oscuro"),("private3.css","Tema Claro")]
        self.css_public.data=kwargs["css_public"]

    def validate_elements_per_page(form,field):
        """ Valida que in input recibido sea un valor entero"""
        try: 
            int(field.data)
            if int(field.data) <= 0 or int(field.data) > 30:
                raise Exception
        except:
            form.elements_per_page.errors = (validators.ValidationError("Debe ingresar un numero entre 1 y 30"),)

    def validate_ordered_by(form,field):
        """" Valida que el input recibido sea un valor dentro de las opciones """
        choices = dict(form.ordered_by.choices).keys()
        if not (field.data in choices):
            form.ordered_by.errors = (validators.ValidationError("Elija una opcion del listado"),)
    
    def validate_css_private(form,field):
        """" Valida que el input recibido sea un valor dentro de las opciones """
        choices = dict(form.css_private.choices).keys()
        if not (field.data in choices):
            form.ordered_by.errors = (validators.ValidationError("Elija una opcion del listado"),)
    
    def validate_css_public(form,field):
        """" Valida que el input recibido sea un valor dentro de las opciones """
        choices = dict(form.css_public.choices).keys()
        if not (field.data in choices):
            form.ordered_by.errors = (validators.ValidationError("Elija una opcion del listado"),)