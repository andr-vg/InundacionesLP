from flask import redirect, render_template, request, url_for, session, abort
from app.models.rol import Rol
from app.models.user import User
from app.helpers.auth import authenticated
from app.db import db

# Protected resources
def index():    
    roles = Rol.query.all()
    return render_template("rol/index.html", roles=roles)


def rol_assign():
    roles = Rol.query.all()
    email=request.form["email"]
    user=User.query.filter(User.email==email).first()
    return render_template("rol/rol_assign.html", user=user, roles=roles)    



def rol_user_assign():
    if not authenticated(session):
        abort(401)
    roles = request.form.getlist("rol")
    email = request.form["email"]
    user = User.query.filter(User.email==email).first()
    for name in roles:
        rol = Rol.query.filter(Rol.name==name).first()
        print(rol)
        user.roles.append(rol)
    db.session.commit()
    return redirect(url_for("user_index"))