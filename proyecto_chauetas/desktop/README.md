# App de escritorio local

Esta carpeta contiene una versión de escritorio de la app de inventario.

## Requisitos

- Node.js 18+ / 20+
- Backend Django en ejecución en `http://127.0.0.1:8000`

## Uso

1. Instala dependencias:

```bash
cd desktop
npm install
```

2. Levanta el backend:

```bash
cd ../backend
python manage.py runserver 127.0.0.1:8000
```

3. Inicia la app de escritorio:

```bash
cd ../desktop
npm start
```

4. (Opcional) Empaqueta la app como ejecutable:

```bash
cd ../desktop
npm run package
```

La app de escritorio se conectará al backend local en `http://127.0.0.1:8000/api`.
