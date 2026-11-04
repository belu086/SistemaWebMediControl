# MediControl

Sistema monolítico modular para la gestión de médicos, pacientes y citas médicas.
**Materia:** TEM-742 Tecnologías Emergentes II — Segundo Parcial Práctico.

Tecnologías: Flask (Application Factory + Blueprints), Flask-SQLAlchemy, Flask-Migrate, SQLite y Bootstrap 5.

## Instalación

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
```

## Base de datos

```bash
set FLASK_APP=run.py           # Linux/Mac: export FLASK_APP=run.py
flask db upgrade               # aplica las migraciones incluidas
python seed.py                 # datos de prueba
```

Si empiezas desde cero: `flask db init`, `flask db migrate -m "Migracion inicial"`, `flask db upgrade`.

## Ejecutar

```bash
python run.py
```

Abrir http://127.0.0.1:5000

## Rutas

| Módulo    | Prefijo     |
|-----------|-------------|
| Médicos   | `/medicos`  |
| Pacientes | `/pacientes`|
| Citas     | `/citas`    |
