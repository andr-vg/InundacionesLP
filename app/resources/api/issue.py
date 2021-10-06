from flask import jsonify, Blueprint

from app.models.issue import Issue

issue_api = Blueprint("consultas", __name__, url_prefix="/consultas")


@issue_api.get("/")
def index():
    return jsonify(issues=[])
