from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField
from wtforms.fields.core import SelectField
    
    
    
class ConfigurationForm(FlaskForm):
    elements_per_page = IntegerField("Elementos por página",[validators.NumberRange(min=1,max=20,message="Numero inválido"),validators.DataRequired(message="Se requiere ingresar un numero de 1 a 20")])
    ordered_by = SelectField("Ordenado por")
    css_private = SelectField("CSS Privado")
    css_public = SelectField("CSS Público")

    def __init__(self,*args,**kwargs):
        super().__init__(*args)
        self.elements_per_page.data =int( kwargs["elements_per_page"])
        self.ordered_by.choices=[("ascendente","Ascendente"),("descendente","Descendente")]
        self.ordered_by.data=kwargs["ordered_by"]
        self.css_private.choices=[("private1.css","Tema Principal"),("private2.css","Tema Oscuro"),("private3.css","Tema Claro")]
        self.css_private.data=kwargs["css_private"]
        self.css_public.choices=[("private1.css","Tema Principal"),("private2.css","Tema Oscuro"),("private3.css","Tema Claro")]
        self.css_public.data=kwargs["css_public"]

    def validate_ordered_by(form,field):
        choices = dict(form.ordered_by.choices).keys()
        print(not (field.data in choices))
        if not (field.data in choices):
            form.ordered_by.errors = (validators.ValidationError("Elija una opcion del listado"),)
    
    def validate_css_private(form,field):
        choices = dict(form.css_private.choices).keys()
        print(not (field.data in choices))
        if not (field.data in choices):
            form.ordered_by.errors = (validators.ValidationError("Elija una opcion del listado"),)
    
    def validate_css_public(form,field):
        choices = dict(form.css_public.choices).keys()
        print(not (field.data in choices))
        if not (field.data in choices):
            form.ordered_by.errors = (validators.ValidationError("Elija una opcion del listado"),)