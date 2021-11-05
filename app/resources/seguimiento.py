from flask import redirect, render_template, request, url_for, session, abort
from flask.helpers import flash
from app.forms.seguimiento import CreateSeguimientoForm
from app.helpers.configuration import get_configuration
from app.helpers.permission import has_permission as check_permission
from app.helpers.email import check as check_email
from app.helpers.auth import authenticated
from sqlalchemy.exc import OperationalError
from app.models.denuncias import Denuncia

from app.models.seguimiento import Seguimiento
from app.models.user import User


def index(page,id):
    """Retorna y renderiza el listado de seguimientos
    :param page:Numero de pagina para el paginado del listado
    :type page: int
    :raises: OperationalError
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("denuncias_index", session):
        abort(401)
    config = get_configuration(session) 
    try:
        seguimientos = Seguimiento.get_tracking(page, config,id)
        denuncia = Denuncia.get_by_id(id)
    except OperationalError:
        flash("No se ha realizado ningun seguimiento a la denuncia aún.")
        seguimientos = None
    return render_template("seguimientos/index.html", denuncia=denuncia,seguimientos=seguimientos)


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
    form = CreateSeguimientoForm()
    return render_template("seguimientos/new.html", denuncia = denuncia,form=form)



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
    user = User.get_user_by_email(authenticated(session))
    form = CreateSeguimientoForm(request.form)
    if form.validate():
        seguimiento = Seguimiento(description=form.description.data)
        denuncia.assign_tracking(seguimiento)
        denuncia.change_state(form.state.data)
        user.assign_tracking(seguimiento)
        seguimiento.update_seguimiento()
    return redirect(url_for("seguimiento_index",page=1,id=denuncia.id))

