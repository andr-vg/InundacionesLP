import datetime
from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.exc import OperationalError
from app.forms.user import RegistrationUserForm,EditUserForm
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
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)

    if not check_permission("user_index", session):
        abort(401)

    # mostramos listado paginado:
    # row con config actual
    config = get_configuration(session) 
    print(config)
    try:
        #users=User.query.filter(User.deleted==False).filter(User.id != id).order_by(User.id.asc()).paginate(page, per_page=config.elements_per_page)
        users=User.get_index_users(id, page, config)
    except OperationalError:
        flash("No hay usuarios aún.")
        users = None
    return render_template("user/index.html", users=users)

def new():
    user_email = authenticated(session)
    #id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("user_new", session):
        abort(401)
    form = RegistrationUserForm()
    form.rol.choices =[(rol.id,rol.name) for rol in Rol.get_all_roles()]
    return render_template("user/new.html", form=form)


def create():
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    form = RegistrationUserForm(request.form)
    form.rol.choices =[(rol.id,rol.name) for rol in Rol.get_all_roles()]
    if form.validate():
        user = User.exists_user(form)
        if user and not user.deleted:
            flash("Ya existe un usuario con ese mail o nombre de usuario. Ingrese uno nuevo.")
            return render_template("user/new.html", form=form)
        elif user and user.deleted:
            user.deleted = False
        else:
            new_user = User(email=form.email.data,password=form.password.data,username=form.username.data,firstname=form.firstname.data,lastname=form.lastname.data)
            db.session.add(new_user)
        for roles in form.rol.data:
                rol = Rol.get_rol_by_id(roles)
                new_user.roles.append(rol)
        db.session.commit()
        flash("El usuario ha sido creado correctamente.")
        return redirect(url_for("user_index"))
    return render_template("user/new.html", form=form)

def edit_user(user, params):
    user.email = params["email"]
    user.username = params["username"]
    user.firstname = params["firstname"]
    user.lastname = params["lastname"]
    user.password = params["password"]
    # ver asignacion y desasignacion de roles

# para mostrar el editar
def edit(id):
    user_email = authenticated(session)
    #user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("user_edit", session):
        abort(401)
    
    #user = User.query.filter(User.id==id).first()
    user = User.get_user_by_id(id)
    return render_template("user/edit.html", user=user)

# para confirmar el editar
def update():
    user_email = authenticated(session)
    user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    # ver si necesita tmb chequear permiso de este boton
    # checkeo de mail valido
    if not User.email_validation(request.form["email"]):
        flash("Ingrese un email valido")
        return render_template("user/edit.html", user=request.form)
    # chequeo que el usuario no exista
    #user = User.query.filter(User.id==request.form["id"]).first()
    user = User.get_user_by_id(request.form["id"])
    # checkeo si el email y username fueron modificados en el form
    if request.form["email"] != user.email:
        # checkeo que no exista ese mail ingresado
        if User.exists_user_with_email(request.form["email"]):
            flash("Ya existe un usuario con ese mail. Ingrese uno nuevo.")
            return render_template("user/edit.html", user=request.form)
    if request.form["username"] != user.username:
        # checkeo que no exista ese username ingresado
        if User.exists_user_with_username(request.form["username"]):
            flash("Ya existe ese nombre de usuario. Ingrese uno nuevo.")
            return render_template("user/edit.html", user=request.form)

    edit_user(user, request.form)
    db.session.commit()
    flash("El usuario ha sido modificado correctamente.")
    return redirect(url_for("user_index"))


def edit():
    user_email = authenticated(session)
    #id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission("user_edit", session):
        abort(401)
    user = User.get_user_by_id(request.form['id'])
    form = EditUserForm(id=user.id,email=user.email,username=user.username,password=user.password,confirm=user.password,firstname=user.firstname,lastname=user.lastname)
    form.rol.choices = [(rol.id,rol.name) for rol in Rol.get_all_roles()]
    form.rol.data = [(rol.id) for rol in user.roles]
    return render_template("user/edit.html", form=form)


def update():
    user_email = authenticated(session)
    #id = User.get_id_from_email(user_email)
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
        user.username = form.username.data
        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
#        user.password = form.password.data
        user_roles = [(rol.id) for rol in user.roles]
        roles_deleted = set(user_roles)-set(form.rol.data)
        for rol in roles_deleted:
            rol_deleted = Rol.get_rol_by_id(rol)
            user.roles.remove(rol_deleted)
        for rol in form.rol.data:
            rol_new = Rol.get_rol_by_id(rol)
            user.roles.append(rol_new)
        db.session.commit()
        return redirect(url_for("user_index"))
    return render_template("user/edit.html", form=form)


def soft_delete(id):
    user_email = authenticated(session)
    #user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission('user_destroy', session):
        abort(401)
    user = User.get_user_by_id(id)
    user.deleted = True
    db.session.commit()
    flash("Usuario eliminado correctamente.")
    return redirect(url_for("user_index"))

def change_state(id):
    user_email = authenticated(session)
    #user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission('user_active', session):
        abort(401)
    #user = User.query.filter(User.id==id).first()
    user = User.get_user_by_id(id)
    user.active = not user.active
    state = "reactivado" if user.active else "bloqueado"
    db.session.commit()
    flash("El usuario ha sido {} correctamente".format(state))
    return redirect(url_for("user_index"))