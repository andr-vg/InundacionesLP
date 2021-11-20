from flask import redirect, render_template, request, url_for, session, abort
from app.models.rol import Rol
from app.models.user import User
from app.helpers.auth import authenticated
from app.db import db

# Protected resources
def index():
    roles = Rol.get_all_roles()
    return render_template("rol/index.html", roles=roles)


def get_session_rol_actual():
    return session["rol_actual"]


def get_session_roles():
    return session["roles"]
