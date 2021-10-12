from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.exc import OperationalError
from app.models.user import User
from app.models.rol import Permission
from app.models.configuration import Configuration
from app.helpers.auth import authenticated
from app.helpers.email import check as check_valid_email
from app.helpers.permission import check as check_permission
from app.helpers.configuration import get_configuration
from app.db import db
from app.resources import rol


# Protected resources
def index(page):
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)

    if not check_permission(id, "user_index"):
        abort(401)

    # mostramos listado paginado:
    # row con config actual
    config = get_configuration(session) 
    print(config)
    try:
        users=User.query.filter(User.deleted==False).order_by(User.id.asc()).paginate(page, per_page=config.elements_per_page)
    except OperationalError:
        flash("No hay usuarios aún.")
        users = None
    return render_template("user/index.html", users=users)

def new():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(id, "user_new"):
        abort(401)
    return render_template("user/new.html", user=None)


def create():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    # ver si necesita tmb chequear permiso de este boton
    # chequeo que el usuario no exista
    if not check_valid_email(request.form["email"]):
        flash("Ingrese un email valido")
        return render_template("user/new.html", user=request.form)
    user = User.exists_user(request.form)
    if user and not user.deleted:
        flash("Ya existe un usuario con ese mail o nombre de usuario. Ingrese uno nuevo.")
        return render_template("user/new.html", user=request.form)
    elif user and user.deleted:
        user.deleted = False
    else:
        new_user = User(**request.form)
        db.session.add(new_user)
    db.session.commit()
    flash("El usuario ha sido creado correctamente.")
    return redirect(url_for("user_index"))

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
    user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(user_id, "user_edit"):
        abort(401)
    
    user = User.query.filter(User.id==id).first()
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
    user = User.query.filter(User.id==request.form["id"]).first()
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


def soft_delete(id):
    user_email = authenticated(session)
    user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(user_id,'user_destroy'):
        abort(401)
    user = User.query.filter(User.id==id).first()
    user.deleted = True
    db.session.commit()
    flash("Usuario eliminado correctamente.")
    return redirect(url_for("user_index"))

def change_state(id):
    user_email = authenticated(session)
    user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(user_id,'user_active'):
        abort(401)
    user = User.query.filter(User.id==id).first()
    user.active = not user.active
    state = "reactivado" if user.active else "bloqueado"
    db.session.commit()
    flash("El usuario ha sido {} correctamente".format(state))
    return redirect(url_for("user_index"))