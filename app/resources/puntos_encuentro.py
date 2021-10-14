from operator import not_
from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.helpers.configuration import get_configuration
from sqlalchemy.exc import OperationalError
from app.forms.puntos_encuentro import CreatePuntoEncuentro, EditPuntoEncuentro
from app.forms.user import EditUserForm
from app.models.puntos_encuentro import PuntosDeEncuentro
from app.models.user import User
from app.helpers.permission import has_permission as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from app.db import db


# Protected resources
def index(page):
    user_email = authenticated(session)
    #id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_index", session):
        abort(401)
    config = get_configuration(session) 
    try:
        puntos_encuentro=PuntosDeEncuentro.get_index_puntos_encuentro(page, config)
    except OperationalError:
        flash("No hay puntos de encuentro aún.")
        puntos_encuentro = None
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)


def new():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_new", session):
        abort(401)
    form = CreatePuntoEncuentro()
    return render_template("puntos_encuentro/new.html", form=form)


def create():
    if not authenticated(session):
        abort(401)
    if not check_permission("punto_encuentro_new", session):
        abort(401)
    form = CreatePuntoEncuentro(request.form)
    if form.validate():
        if PuntosDeEncuentro.unique_fields(request.form):
            flash("Uno o mas campos ya se encuentra cargado en el sistema")
            return render_template("puntos_encuentro/new.html", form=form)
        new_punto = PuntosDeEncuentro(name=form.name.data.upper(),address=form.address.data.upper(),tel=form.tel.data,email=form.email.data,coords=form.coords.data)
        db.session.add(new_punto)
        db.session.commit()
        return redirect(url_for("punto_encuentro_index"))
    return render_template("puntos_encuentro/new.html",form=form)


def search():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_index", session):
        abort(401)
    config = get_configuration(session)
    puntos_encuentro = PuntosDeEncuentro.search_by_name(request.args["name"])
    if "active" in request.args.keys():
        puntos_encuentro = PuntosDeEncuentro.filter_by_state(puntos_encuentro,request.args["active"])
    return render_template("puntos_encuentro/index.html", puntos_encuentro=puntos_encuentro)


def edit():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    punto = PuntosDeEncuentro.get_punto_by_id(request.form['id'])
    form = EditPuntoEncuentro(id=punto.id,name=punto.name,address=punto.address,tel=punto.tel,email=punto.email,coords=punto.coords)
    return render_template("puntos_encuentro/edit.html", form=form)


def update():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("punto_encuentro_update", session):
        abort(401)
    form = EditPuntoEncuentro(request.form)
    if form.validate:
        punto = PuntosDeEncuentro.get_punto_by_id(form.id.data)
        query = PuntosDeEncuentro.get_punto_by_name(form.name.data)
        if query and punto.id!=query.id:
            flash("Ya se encuentra un punto de encuentro con dicho nombre en el sistema")
            return render_template("puntos_encuentro/new.html", form=form)
        query = PuntosDeEncuentro.get_punto_by_address(form.address.data)
        if query and punto.id!=query.id:
            flash("Ya se encuentra un punto de encuentro con dicha direccion en el sistema")
            return render_template("puntos_encuentro/new.html", form=form)
        punto.name = form.name.data.upper()
        punto.address = form.address.data.upper()
        punto.tel = form.tel.data
        punto.email = form.email.data
        punto.coords = form.coords.data
        db.session.commit()
        return redirect(url_for("punto_encuentro_index"))
    return render_template("puntos_encuentro/new.html", form=form)


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
    