from os import path, environ
from flask import Flask, render_template, g, Blueprint
from flask_session import Session
from config import config
from app import db
from flask_bcrypt import Bcrypt
from app.resources import configuration, issue, puntos_encuentro, user, auth, rol
from app.resources.api.issue import issue_api
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers import permission as helper_permission
import logging



def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    
    # Carga libreria para encriptar las contraseñas
#    bcrypt = Bcrypt(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)

    #Logs de la BD
    #logging.basicConfig()
    #logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_permission.has_permission)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Consultas
    app.add_url_rule("/consultas", "issue_index", issue.index)
    app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index, defaults={'page': 1}, methods=['GET'])
    app.add_url_rule("/usuarios/<int:page>", "user_index", user.index, methods=['GET'])
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/editar", "user_edit", user.edit,methods=["POST"])
    app.add_url_rule("/usuarios/actualizar", "user_update", user.update, methods=["POST"])
    app.add_url_rule("/usuarios/eliminar/<int:id>", "user_soft_delete", user.soft_delete, methods=["POST"])
    app.add_url_rule("/usuarios/estado/<int:id>", "user_change_state", user.change_state)
    app.add_url_rule("/usuarios/search/", "user_search", user.search, defaults={'page': 1}, methods=['GET'])
    app.add_url_rule("/usuarios/search/<int:page>", "user_search", user.search, methods=['GET'])
    app.add_url_rule("/usuarios/cambiar_rol", "user_change_rol", user.change_rol, methods=["POST"])

    # Rutas de perfil propio
    app.add_url_rule("/perfil", "user_edit_profile", user.edit_profile)
    app.add_url_rule("/actualizar_perfil", "user_update_profile", user.update_profile, methods=["POST"])

    # Rutas de Roles

   

    # Rutas de Puntos de encuentro
    app.add_url_rule("/puntos_encuentro", "punto_encuentro_index", puntos_encuentro.index, defaults={'page': 1}, methods=['GET'])
    app.add_url_rule("/puntos_encuentro/<int:page>", "punto_encuentro_index", puntos_encuentro.index, methods=['GET'])
    app.add_url_rule("/puntos_encuentro/search/", "punto_encuentro_search", puntos_encuentro.search)
    app.add_url_rule("/puntos_encuentro", "punto_encuentro_create", puntos_encuentro.create, methods=["POST"])
    app.add_url_rule("/puntos_encuentro/nuevo", "punto_encuentro_new", puntos_encuentro.new)
    app.add_url_rule("/puntos_encuentro/editar", "punto_encuentro_edit", puntos_encuentro.edit, methods=["POST"])
    app.add_url_rule("/puntos_encuentro/actualizar", "punto_encuentro_update", puntos_encuentro.update, methods=["POST"])
    app.add_url_rule("/puntos_encuentro/eliminar", "punto_encuentro_soft_delete", puntos_encuentro.soft_delete,methods=["POST"])
    app.add_url_rule("/puntos_encuentro/publicar", "punto_encuentro_publish", puntos_encuentro.publish,methods=["POST"])


    # Rutas de Configuracion
    app.add_url_rule("/configuracion", "configuration_update", configuration.update)
    app.add_url_rule("/config", "configuration_confirm_update", configuration.confirm_update, methods=["POST"])

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")

    # Rutas de API-REST (usando Blueprints)
    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(issue_api)

    app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app
