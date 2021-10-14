from operator import not_
from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.models.puntos_encuentro import PuntosDeEncuentro
from app.models.user import User
from app.helpers.permission import has_permission as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from app.db import db


# Protected resources
def index():
    user_email = authenticated(session)
    #id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_index", session):
        abort(401)
    puntos_encuentro = PuntosDeEncuentro.get_all()
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)


def new():
    user_email = authenticated(session)
    #id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_new", session):
        abort(401)
    return render_template("puntos_encuentro/new.html", puntos_encuentro=None)


def create():
    if not authenticated(session):
        abort(401)
    if not check_email(request.form["email"]):
        flash("Ingrese un email valido")
        return render_template("puntos_encuentro/new.html", puntos_encuentro=request.form)
    if PuntosDeEncuentro.unique_fields(request.form):
        flash("Uno o mas campos ya se encuentra cargado en el sistema")
        return render_template("puntos_encuentro/new.html", puntos_encuentro=request.form)
    new_punto = PuntosDeEncuentro(**request.form)
    db.session.add(new_punto)
    db.session.commit()
    return redirect(url_for("punto_encuentro_index"))

def search():
    user_email = authenticated(session)
    #id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_index", session):
        abort(401)
    puntos_encuentro = PuntosDeEncuentro.search_by_name(request.args["name"])
    if "active" in request.args.keys():
        if request.args["active"]=="activo":
            puntos_encuentro = puntos_encuentro.filter(PuntosDeEncuentro.state==False)
        if request.args["active"]=="inactivo":
            puntos_encuentro = puntos_encuentro.filter(PuntosDeEncuentro.state==True)
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)


def soft_delete():
    user_email = authenticated(session)
    print(session.get("permissions"))
    if not user_email:
        abort(401)
    if not check_permission('punto_encuentro_destroy',session):
        abort(401)
    punto_encuentro = PuntosDeEncuentro.get_punto_by_id(request.form['id'])
    punto_encuentro.state = True
    db.session.commit()
    flash("Punto de encuentro de encuentro despublicado")
    return redirect(url_for("punto_encuentro_index"))

def publish():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('punto_encuentro_publish',session):
        abort(401)
    punto_encuentro = PuntosDeEncuentro.get_punto_by_id(request.form['id'])
    punto_encuentro.state = False
    db.session.commit()
    flash("Punto de encuentro de encuentro publicado")
    return redirect(url_for("punto_encuentro_index"))
    
def show(name):
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_show", session):
        abort(401)
    
    punto = PuntosDeEncuentro.get_punto_by_name(name)
    return render_template("puntos_encuentro/show.html", pto=punto)