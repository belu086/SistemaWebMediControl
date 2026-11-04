from flask import render_template, request, redirect, url_for, flash

from app import db
from app.models import Medico
from app.medicos import bp_medicos


@bp_medicos.route("/")
def listar():
    medicos = Medico.query.order_by(Medico.id).all()
    return render_template("medicos/listar.html", medicos=medicos)


@bp_medicos.route("/nuevo", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        especialidad = request.form["especialidad"].strip()
        if not nombre or not especialidad:
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("medicos/form.html", medico=None)
        db.session.add(Medico(nombre=nombre, especialidad=especialidad))
        db.session.commit()
        flash("Médico registrado correctamente.", "success")
        return redirect(url_for("medicos.listar"))
    return render_template("medicos/form.html", medico=None)


@bp_medicos.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    medico = Medico.query.get_or_404(id)
    if request.method == "POST":
        medico.nombre = request.form["nombre"].strip()
        medico.especialidad = request.form["especialidad"].strip()
        db.session.commit()
        flash("Médico actualizado correctamente.", "success")
        return redirect(url_for("medicos.listar"))
    return render_template("medicos/form.html", medico=medico)


@bp_medicos.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    medico = Medico.query.get_or_404(id)
    db.session.delete(medico)
    db.session.commit()
    flash("Médico eliminado.", "warning")
    return redirect(url_for("medicos.listar"))
