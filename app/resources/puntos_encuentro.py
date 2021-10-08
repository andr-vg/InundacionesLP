from flask import redirect, render_template, request, url_for, session, abort
from app.models.puntos_encuentro import PuntosDeEncuentro
from app.helpers.auth import authenticated
from app.db import db


# Protected resources
def index():
#    if not authenticated(session):
#        abort(401)
    puntos_encuentro = PuntosDeEncuentro.query.all()
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)


def new():
#    if not authenticated(session):
#        abort(401)
    return render_template("puntos_encuentro/new.html")


def create():
#    if not authenticated(session):
#        abort(401)
    new_punto = PuntosDeEncuentro(**request.form)
    db.session.add(new_punto)
    db.session.commit()
    return redirect(url_for("puntos_encuentro_index"))