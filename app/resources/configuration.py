from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.configuration import Configuration
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.permission import check as check_permission
from app.db import db

def update():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(id, "configuration_update"):
        abort(401)
    config=Configuration.query.first()
    return render_template("configuration/update.html",config=config)
    

def confirm_update():
    config=Configuration.query.first()
    config.elements_per_page = request.form["elements_per_page"]
    config.ordered_by = request.form["ordered_by"]
    config.css_private = request.form["css_private"]
    config.css_public = request.form["css_public"]
    db.session.commit()
    flash("La configuracion ha sido guardada")
    return  redirect(url_for("configuration_update"))