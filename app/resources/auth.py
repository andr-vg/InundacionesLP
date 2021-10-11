from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User
from app.models.configuration import Configuration
from sqlalchemy import and_


def login():
    return render_template("auth/login.html")


def authenticate():

    params=request.form

    user=(User.query.filter(and_(User.deleted==False,User.active==True)) 
    .filter(and_(User.email == params["email"],User.password == params["password"])).first()
    )
    print(user)
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    session["user"] = user.email
    # save configuration params to 
    session["config"] = Configuration.query.filter().first()
    flash("La sesión se inició correctamente.")

    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))

