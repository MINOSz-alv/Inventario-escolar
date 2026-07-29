#!/usr/bin/env python3
"""Inicializa la base de datos Mongo local para la app.
Lee `inventory/fixtures/initial_data.json` (formato Django fixtures) e inserta
categorías, ubicaciones y items en las colecciones `categories`, `locations`, `items`.
Crea índices y opcionalmente crea un usuario MongoDB si se proporcionan
`MONGO_INIT_USER` y `MONGO_INIT_PWD` (requiere privilegios de admin).
"""
import os
import json
from datetime import datetime, timezone
from pymongo import MongoClient
from bson import ObjectId

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FIXTURE_PATH = os.path.join(BASE_DIR, 'inventory', 'fixtures', 'initial_data.json')

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB_NAME', 'cecytem_db')
MONGO_INIT_USER = os.getenv('MONGO_INIT_USER')
MONGO_INIT_PWD = os.getenv('MONGO_INIT_PWD')
CREATE_MONGO_USER = os.getenv('CREATE_MONGO_USER', 'false').lower() in ('1','true','yes')

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

categories = db.categories
locations = db.locations
items = db.items


def parse_iso(s):
    if s is None:
        return None
    # Handle trailing Z
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(s)
    except Exception:
        # fallback: naive attempt
        try:
            return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
        except Exception:
            return None


def load_fixtures(path=FIXTURE_PATH):
    if not os.path.exists(path):
        print(f'No se encontró fixtures en {path}')
        return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Keep mapping from old PK to new ObjectId
    cat_map = {}
    loc_map = {}

    # First pass: categories and locations
    for entry in data:
        model = entry.get('model')
        pk = entry.get('pk')
        fields = entry.get('fields', {})
        if model.endswith('category'):
            doc = {'name': fields.get('name')}
            res = categories.insert_one(doc)
            cat_map[pk] = res.inserted_id
        elif model.endswith('location'):
            doc = {'name': fields.get('name')}
            res = locations.insert_one(doc)
            loc_map[pk] = res.inserted_id

    # Second pass: items
    for entry in data:
        model = entry.get('model')
        fields = entry.get('fields', {})
        if model.endswith('item'):
            created_at = parse_iso(fields.get('created_at')) or datetime.utcnow()
            doc = {
                'name': fields.get('name'),
                'description': fields.get('description', ''),
                'quantity': fields.get('quantity', 0),
                'category_id': cat_map.get(fields.get('category')) if fields.get('category') else None,
                'location_id': loc_map.get(fields.get('location')) if fields.get('location') else None,
                'created_at': created_at,
            }
            items.insert_one(doc)

    print('Fixtures cargadas:')
    print(f'  categories: {categories.count_documents({})}')
    print(f'  locations:  {locations.count_documents({})}')
    print(f'  items:      {items.count_documents({})}')


def create_indexes():
    print('Creando índices...')
    items.create_index([('created_at', -1)])
    items.create_index('category_id')
    items.create_index('location_id')
    try:
        items.create_index([('name', 'text'), ('description', 'text')])
    except Exception:
        # Some Mongo versions may not allow combined text index creation if one exists
        pass
    print('Índices creados')


def create_mongo_user(user, pwd, dbname):
    try:
        admin_db = client['admin']
        admin_db.command('createUser', user, pwd=pwd, roles=[{'role': 'readWrite', 'db': dbname}])
        print(f'Usuario {user} creado con rol readWrite en {dbname}')
    except Exception as e:
        print('No se pudo crear usuario (¿privilegios insuficientes?):', e)


if __name__ == '__main__':
    print('Conectando a', MONGO_URI, 'DB=', MONGO_DB)
    load_fixtures()
    create_indexes()
    if CREATE_MONGO_USER and MONGO_INIT_USER and MONGO_INIT_PWD:
        create_mongo_user(MONGO_INIT_USER, MONGO_INIT_PWD, MONGO_DB)
    print('Inicialización completada.')
