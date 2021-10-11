from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.rol import Permission
from app.helpers.auth import authenticated
from app.helpers.email import check as check_valid_email
from app.helpers.permission import check as check_permission
from app.db import db
from app.resources import rol


# Protected resources
def index():
    user_email = authenticated(session)
    id = User.get_id_from_email(user_email)
    if not user_email:
        abort(401)

    if not check_permission(id, "user_index"):
        abort(401)
        
    users=User.query.filter(User.deleted==False)
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