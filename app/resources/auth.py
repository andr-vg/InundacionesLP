from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User, Rol
from app.models.configuration import Configuration
from sqlalchemy import and_
from app.helpers.auth import authenticated as auth
from app.helpers.permission import has_permission as perm

from app.resources import rol


def login():
    return render_template("auth/login.html")


def authenticate():
    params = request.form
    user = User.login(params=params)
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))
    session["user"] = user.email
    session["username"] = user.username
    session["config"] = Configuration.get_configuration()
    session["permissions"] = User.get_permissions(user_id=user.id)
    flash("La sesión se inició correctamente.")

    return render_template("home.html")


def authenticated():
    return auth(session)


def has_permission(permission):
    return perm(permission, session)


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))
