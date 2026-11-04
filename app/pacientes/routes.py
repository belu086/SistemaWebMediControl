from flask import render_template, request, redirect, url_for, flash

from app import db
from app.models import Paciente
from app.pacientes import bp_pacientes


@bp_pacientes.route("/")
def listar():
    pacientes = Paciente.query.order_by(Paciente.id).all()
    return render_template("pacientes/listar.html", pacientes=pacientes)


@bp_pacientes.route("/nuevo", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        telefono = request.form["telefono"].strip()
        if not nombre or not telefono:
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("pacientes/form.html", paciente=None)
        db.session.add(Paciente(nombre=nombre, telefono=telefono))
        db.session.commit()
        flash("Paciente registrado correctamente.", "success")
        return redirect(url_for("pacientes.listar"))
    return render_template("pacientes/form.html", paciente=None)


@bp_pacientes.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    paciente = Paciente.query.get_or_404(id)
    if request.method == "POST":
        paciente.nombre = request.form["nombre"].strip()
        paciente.telefono = request.form["telefono"].strip()
        db.session.commit()
        flash("Paciente actualizado correctamente.", "success")
        return redirect(url_for("pacientes.listar"))
    return render_template("pacientes/form.html", paciente=paciente)


@bp_pacientes.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash("Paciente eliminado.", "warning")
    return redirect(url_for("pacientes.listar"))
