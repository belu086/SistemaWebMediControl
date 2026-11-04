from datetime import datetime

from flask import render_template, request, redirect, url_for, flash

from app import db
from app.models import Cita, Medico, Paciente
from app.citas import bp_citas


def _leer_formulario():
    fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
    hora = datetime.strptime(request.form["hora"], "%H:%M").time()
    return fecha, hora, int(request.form["medico_id"]), int(request.form["paciente_id"])


@bp_citas.route("/")
def listar():
    citas = Cita.query.order_by(Cita.fecha, Cita.hora).all()
    return render_template("citas/listar.html", citas=citas)


@bp_citas.route("/nueva", methods=["GET", "POST"])
def crear():
    medicos = Medico.query.order_by(Medico.nombre).all()
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    if request.method == "POST":
        fecha, hora, medico_id, paciente_id = _leer_formulario()
        ocupada = Cita.query.filter_by(medico_id=medico_id, fecha=fecha, hora=hora).first()
        if ocupada:
            flash("El médico ya tiene una cita en esa fecha y hora.", "danger")
            return render_template("citas/form.html", cita=None, medicos=medicos, pacientes=pacientes)
        db.session.add(Cita(fecha=fecha, hora=hora, medico_id=medico_id, paciente_id=paciente_id))
        db.session.commit()
        flash("Cita registrada correctamente.", "success")
        return redirect(url_for("citas.listar"))
    return render_template("citas/form.html", cita=None, medicos=medicos, pacientes=pacientes)


@bp_citas.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    cita = Cita.query.get_or_404(id)
    medicos = Medico.query.order_by(Medico.nombre).all()
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    if request.method == "POST":
        fecha, hora, medico_id, paciente_id = _leer_formulario()
        ocupada = Cita.query.filter(
            Cita.medico_id == medico_id, Cita.fecha == fecha, Cita.hora == hora, Cita.id != id
        ).first()
        if ocupada:
            flash("El médico ya tiene una cita en esa fecha y hora.", "danger")
            return render_template("citas/form.html", cita=cita, medicos=medicos, pacientes=pacientes)
        cita.fecha, cita.hora = fecha, hora
        cita.medico_id, cita.paciente_id = medico_id, paciente_id
        db.session.commit()
        flash("Cita actualizada correctamente.", "success")
        return redirect(url_for("citas.listar"))
    return render_template("citas/form.html", cita=cita, medicos=medicos, pacientes=pacientes)


@bp_citas.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    flash("Cita cancelada.", "warning")
    return redirect(url_for("citas.listar"))
