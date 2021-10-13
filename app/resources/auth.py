from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User, Rol
from app.models.configuration import Configuration
from sqlalchemy import and_


def login():
    return render_template("auth/login.html")


def authenticate():
    params=request.form
 #   user=(User.query.filter(and_(User.deleted==False,User.active==True)) 
 #   .filter(and_(User.email == params["email"],User.password == params["password"])).first()
 #   )
    #user=Configuration.query.filter(and_(Configuration.elements_per_page==params["email"],Configuration.ordered_by==params["password"]))
    user = User.login(params=params)
    
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))
    session["user"] = user.email
    session["username"] = user.username
    # save configuration params 
    session["config"] = Configuration.get_configuration()
    # save roles from this user
    roles = [(rol.id, rol.name) for rol in user.roles]
    print(roles)
    session["roles"] = roles
    # assign the permissions of the first rol by default
    #rol_id = next(iter(roles))
    rol_id = roles[0][0]
    print(rol_id)
    # save permissions
    session["permissions"] = Rol.get_permissions(rol_id=rol_id)
    print(session["permissions"])
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))

