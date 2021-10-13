from flask import redirect, render_template, request, url_for, session, abort, flash
from sqlalchemy.exc import OperationalError
from app.forms.user import RegistrationUserForm
from app.models.user import User
from app.models.rol import Rol
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
    form = RegistrationUserForm()
    form.rol.choices =[(rol.id,rol.name) for rol in Rol.get_all_roles()]
    if not user_email:
        abort(401)
    if not check_permission(id, "user_new"):
        abort(401)
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


def soft_delete(id):
    user_email = authenticated(session)
    user_id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)
    if not check_permission(user_id,'user_destroy'):
        abort(401)
    user = User.get_user_by_id(id)
    user.deleted = True
    db.session.commit()
    flash("Usuario eliminado correctamente.")
    return redirect(url_for("user_index"))