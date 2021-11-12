import datetime
import bcrypt
from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.exc import OperationalError
from app.forms.user import RegistrationUserForm,EditUserForm,EditProfileForm
from app.models.user import User
from app.models.rol import Rol
from app.models.configuration import Configuration
from app.helpers.auth import authenticated
from app.helpers.email import check as check_valid_email
from app.helpers.permission import has_permission as check_permission
from app.helpers.configuration import get_configuration
from app.db import db
from app.resources import rol


# Protected resources
def index(page):
    """
    Renderizado del listado de usuarios de forma paginada

    Args:
        page(int): número de pagina
    """
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)

    if not check_permission("user_index", session):
        abort(401)

    # mostramos listado paginado:
    # row con config actual
    config = get_configuration(session) 
    try:
        users=User.get_index_users(id, page, config)
    except OperationalError:
        flash("No hay usuarios aún.")
        users = None
    return render_template("user/index.html", users=users)

def new():
    """
    Renderizado de la página de creación de un usuario
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("user_new", session):
        abort(401)
    form = RegistrationUserForm()
    form.rol.choices =[(rol.id,rol.name) for rol in Rol.get_all_roles()]
    return render_template("user/new.html", form=form)


def create():
    """
    Lógica a realizar al momento de confirmar
    la creación de un usuario 
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    form = RegistrationUserForm(request.form)
    form.rol.choices =[(rol.id,rol.name) for rol in Rol.get_all_roles()]
    if form.validate():
        parameters = {"email":form.email, "username": form.username}
        user = User.exists_user(parameters)
        if user and not user.deleted:
            flash("Ya existe un usuario con ese mail o nombre de usuario. Ingrese uno nuevo.")
            return render_template("user/new.html", form=form)
        elif user and user.deleted:
            user.activate()
            user.update()
        else:
            new_user = User(email=form.email.data,password=form.password.data,username=form.username.data,firstname=form.firstname.data,lastname=form.lastname.data)
            new_user.add_user()
            new_user.update()
        for roles in form.rol.data:
            rol = Rol.get_rol_by_id(roles)
            new_user.add_rol(rol)
            new_user.update()
        flash("El usuario ha sido creado correctamente.")
        return redirect(url_for("user_index"))
    return render_template("user/new.html", form=form)


def edit():
    """
    Renderizado de la página de edición de un usuario
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("user_edit", session):
        abort(401)
    user = User.get_user_by_id(request.form['id'])
    form = EditUserForm(id=user.id,email=user.email,username=user.username,firstname=user.firstname,lastname=user.lastname)
    form.rol.choices = [(rol.id,rol.name) for rol in Rol.get_all_roles()]
    form.rol.data = [(rol.id) for rol in user.roles]
    return render_template("user/edit.html", form=form)


def update():
    """
    Lógica a realizar al momento de confirmar
    la edición de un usuario 
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("user_update", session):
        abort(401)
    form = EditUserForm(request.form)
    form.rol.choices = [(rol.id,rol.name) for rol in Rol.get_all_roles()]
    if form.validate():
        user = User.get_user_by_id(form.id.data)
        query = User.get_user_by_email(form.email.data)
        if query and query.id!=user.id:
            flash("Ya existe un usuario con dicho email")
            return render_template("user/edit.html", form=form)
        query = User.get_user_by_username(form.username.data)
        if query and query.id!=user.id:
            flash("Ya existe un usuario con dicho nombre de usuario")
            return render_template("user/edit.html", form=form)
        user_roles = [(rol.id) for rol in user.roles]
        roles_deleted = set(user_roles)-set(form.rol.data)
        user.edit_user(form, roles_deleted)
        user.update()
        flash("El usuario ha sido editado correctamente.")
        return redirect(url_for("user_index"))
    return render_template("user/edit.html", form=form)


def soft_delete():
    """
    Lógica a realizar al momento de eliminar
    de manera lógica a un usuario

    Args:
        id(int): id del usuario a eliminar
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('user_destroy', session):
        abort(401)
    user = User.get_user_by_id(request.form["id"])
    user.delete()
    user.update()
    flash("Usuario eliminado correctamente.")
    return redirect(url_for("user_index"))

def change_state(id):
    """
    Lógica a realizar al momento de modificar el
    estado de un usuario.

    Args:
        id(int): id del usuario 
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission('user_active', session):
        abort(401)
    user = User.get_user_by_id(id)
    user.change_state()
    state = "reactivado" if user.active else "bloqueado"
    user.update()
    flash("El usuario ha sido {} correctamente".format(state))
    return redirect(url_for("user_index"))

def search(page):
    """
    Lógica a realizar al momento de renderizar
    un listado de búsqueda de usuarios paginado.

    Args:
        page(int): número de página
    """
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("user_index",session):
        abort(401)
    config = get_configuration(session) 
    users = User.search_by_name(request.args["name"])
    name = request.args["name"]
    active = ""
    if "active" in request.args.keys() and request.args["active"]!="":
        active = request.args["active"]
        if request.args["active"]=="activo":
            users = User.get_with_state(users, True)
        elif request.args["active"]=="bloqueado":
            users = User.get_with_state(users, False)
    users = User.search_paginate(users, id, page, config)

    return render_template("user/index.html", users=users, filter=1, name=name, active=active)

def edit_profile():
    """
    Renderizado de la página de edición del perfil de usuario
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("user_edit_profile", session):
        abort(401)
    
    user = User.get_user_by_email(user_email)
    form = EditProfileForm(id=user.id,firstname=user.firstname,lastname=user.lastname)
    return render_template("user/profile.html", form=form)


def update_profile():
    """
    Lógica a realizar al momento de confirmar
    la edición del perfil del usuario actual.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("user_update_profile", session):
        abort(401)
    form = EditProfileForm(request.form)
    if form.validate():
        user = User.get_user_by_id(form.id.data)
        user.edit_profile(form)
        user.update()
        flash("Su perfil ha sido actualizado.")
        return redirect(url_for("home"))       
    return render_template("user/profile.html", form=form)

def show(username):
    """
    Renderiza el detalle con los datos de un dado usuario

    Args:
        username(string): nombre del usuario a detallar
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission("user_show", session):
        abort(401)
    
    user = User.get_user_by_username(username)
    return render_template("user/show.html", user=user)

def get_session_username():
    return session["username"]
