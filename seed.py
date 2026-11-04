"""Datos de prueba. Ejecutar con:  python seed.py"""
from datetime import date, time

from app import create_app, db
from app.models import Medico, Paciente, Cita

app = create_app()

with app.app_context():
    if Medico.query.count() == 0:
        medicos = [
            Medico(nombre="Dr. Juan Gracia", especialidad="Cirujano"),
            Medico(nombre="Dr. leandro Silva", especialidad="Pediatría"),
            Medico(nombre="Dra. Marta Perez", especialidad="Traumatología"),
            Medico(nombre="Dra. Ana Condori", especialidad="Dermatología"),
        ]
        pacientes = [
            Paciente(nombre="joana larico", telefono="7236567"),
            Paciente(nombre="pedro mamani", telefono="72345678"),
            Paciente(nombre="rosario palca", telefono="73456789"),
            Paciente(nombre="hernan fernandez", telefono="74567890"),
            Paciente(nombre="ana catacora", telefono="75678901"),
        ]
        db.session.add_all(medicos + pacientes)
        db.session.commit()

        citas = [
            Cita(fecha=date(2026, 11, 10), hora=time(9, 0), medico_id=medicos[0].id, paciente_id=pacientes[0].id),
            Cita(fecha=date(2026, 11, 11), hora=time(11, 30), medico_id=medicos[1].id, paciente_id=pacientes[1].id),
            Cita(fecha=date(2026, 11, 12), hora=time(7, 30), medico_id=medicos[2].id, paciente_id=pacientes[2].id),
            Cita(fecha=date(2026, 11, 12), hora=time(13, 0), medico_id=medicos[3].id, paciente_id=pacientes[3].id),
            Cita(fecha=date(2026, 11, 13), hora=time(16, 0), medico_id=medicos[0].id, paciente_id=pacientes[4].id),
        ]
        db.session.add_all(citas)
        db.session.commit()
        print("Datos de prueba insertados.")
    else:
        print("La base de datos ya tiene datos.")
