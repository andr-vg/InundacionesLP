from flask import redirect, render_template, request, url_for, session, abort
from app.models.rol import Rol
from app.helpers.auth import authenticated

# Protected resources
def index():    
    return render_template("rol/index.html", roles=[])


def new():
    if not authenticated(session):
        abort(401)

    return render_template("user/new.html")


def create():
    if not authenticated(session):
        abort(401)

    conn = connection()
    Rol.create(conn, request.form)
    return redirect(url_for("user_index"))
