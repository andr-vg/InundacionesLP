from flask import redirect, render_template, request, url_for, session, abort
from app.models.rol import Rol
from app.models.user import User
from app.helpers.auth import authenticated
from app.db import db

# Protected resources
def index():    
    roles = Rol.query.all()
    return render_template("rol/index.html", roles=roles)


def rol_assign(id):
    roles = Rol.query.all()
    user=User.query.filter(User.id==id).first()
    return render_template("rol/rol_assign.html", user=user, roles=roles)    


def rol_user_assign():
    if not authenticated(session):
        abort(401)
    roles = request.form.getlist("rol")
    user = User.get_user_by_id(request.form['id'])
    for name in roles:
        rol = Rol.query.filter(Rol.name==name).first()
        user.roles.append(rol)
    db.session.commit()
    return redirect(url_for("user_index"))