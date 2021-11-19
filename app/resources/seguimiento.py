from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.forms.seguimiento import CreateSeguimientoForm
from app.helpers.configuration import get_configuration
from app.helpers.permission import has_permission as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from sqlalchemy.exc import OperationalError
from app.models.denuncias import Denuncia
from app.models.categories import Categoria
from app.models.seguimiento import Seguimiento
from app.models.user import User




def new(id):
    """Retorna y renderiza el formulario para la creacion de un seguimiento"""
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncias_update", session):
        abort(401)
    denuncia = Denuncia.get_by_id(id)
    if not denuncia: 
        abort(400)
    if denuncia.is_closed():
        abort(400)
    if denuncia.is_resolved():
        abort(400)
    form = CreateSeguimientoForm()
    return render_template("seguimientos/new.html", denuncia = denuncia,user=denuncia.user_assign,form=form)



def create(id):
    """Contiene la logica para la creacion de un nuevo seguimiento, 
    si el formulario es valido se carga en la base de datos."""
    if not authenticated(session):
        abort(401)
    if not check_permission("denuncias_update", session):
        abort(401)
    denuncia = Denuncia.get_by_id(id)
    if not denuncia: 
        abort(400)
    if denuncia.is_closed():
        abort(400)
    if denuncia.is_resolved():
        abort(400)
    user = User.get_user_by_email(authenticated(session))
    form = CreateSeguimientoForm(request.form)
    if form.validate():
        seguimiento = Seguimiento(description=form.description.data)
        seguimiento.add()
        denuncia.assign_tracking(seguimiento)
        user.assign_tracking(seguimiento)
        return redirect(url_for("denuncia_tracking"))
    return render_template("seguimientos/new.html", denuncia = denuncia,user=denuncia.user_assign,form=form)



def delete(page,id):
    """  Eliminacion de un seguimiento"""
    if not authenticated(session):
        abort(401)
    if not check_permission("denuncias_destroy", session):
        abort(401)
    seguimiento = Seguimiento.get_by_id(id)
    if not seguimiento:
        abort(400)
    denuncia = seguimiento.complaints
    seguimiento.delete_tracking()
    return redirect(url_for("denuncia_show", id=denuncia.id))

