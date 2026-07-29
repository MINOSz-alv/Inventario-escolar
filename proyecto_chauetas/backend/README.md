# Backend (Django + DRF)

Instrucciones rápidas:

1. Crear y activar virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Migrar y ejecutar:

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

La API estará en `http://localhost:8000/api/`.

Credenciales de prueba (desarrollo):

- admin / adminpass (superuser creado automáticamente por el asistente)

Para cargar datos de ejemplo:

```bash
./.venv/bin/python manage.py loaddata inventory/fixtures/initial_data.json
```

Ejecutar tests:

```bash
./.venv/bin/python manage.py test
```
