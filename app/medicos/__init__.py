from flask import Blueprint

bp_medicos = Blueprint("medicos", __name__)

from app.medicos import routes  # noqa: E402,F401
