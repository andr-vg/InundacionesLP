from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.configuration import Configuration
from app.forms.configuration import ConfigurationForm
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.permission import has_permission as check_permission
from app.helpers.configuration import get_configuration as help_configuration
from app.db import db

def update(): 
    """" Renderiza el formulario para la actualización de la configuracion del sistema  """
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("configuration_update", session):
        abort(401)
    config = Configuration.get_configuration()
    form = ConfigurationForm(elements_per_page=config.elements_per_page,ordered_by=config.ordered_by,css_private=config.css_private,css_public=config.css_public)
    return render_template("configuration/update.html",form=form)
    

def confirm_update():
    """" Actualiza la configuración del sistema en la base de datos """
    config=Configuration.get_configuration()
    form = ConfigurationForm(elements_per_page=request.form["elements_per_page"],ordered_by=request.form["ordered_by"],css_private=request.form["css_private"],css_public=request.form["css_public"])
    if form.validate():
        config.elements_per_page = request.form["elements_per_page"]
        config.ordered_by = request.form["ordered_by"]
        config.css_private = request.form["css_private"]
        config.css_public = request.form["css_public"]
        db.session.commit()
    # actualizo los params de configuracion en la sesión
        session["config"] = Configuration.get_configuration()
        flash("La configuracion ha sido guardada")
        return render_template("configuration/update.html",form=form) 
    return render_template("configuration/update.html",form=form) 

def get_session_configuration():
    return help_configuration(session)

