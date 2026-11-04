import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from jinja2 import ChoiceLoader, FileSystemLoader, PrefixLoader

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Cada módulo tiene su carpeta templates: se usan como "medicos/listar.html", etc.
    app.jinja_loader = ChoiceLoader([
        app.jinja_loader,
        PrefixLoader({
            nombre: FileSystemLoader(os.path.join(app.root_path, nombre, "templates"))
            for nombre in ("medicos", "pacientes", "citas")
        }),
    ])

    from app import models  # noqa: F401

    from app.medicos import bp_medicos
    from app.pacientes import bp_pacientes
    from app.citas import bp_citas

    app.register_blueprint(bp_medicos, url_prefix="/medicos")
    app.register_blueprint(bp_pacientes, url_prefix="/pacientes")
    app.register_blueprint(bp_citas, url_prefix="/citas")

    @app.route("/")
    def index():
        from app.models import Medico, Paciente, Cita
        return render_template(
            "inicio.html",
            total_medicos=Medico.query.count(),
            total_pacientes=Paciente.query.count(),
            total_citas=Cita.query.count(),
            citas=Cita.query.order_by(Cita.id.desc()).limit(5).all(),
        )

    return app
