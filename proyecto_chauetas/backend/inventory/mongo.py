from datetime import datetime
from django.conf import settings
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

categories = db.categories
locations = db.locations
items = db.items


def to_object_id(value):
    if value is None or value == '':
        return None
    try:
        return ObjectId(value)
    except Exception as exc:
        raise ValueError('ID inválido') from exc


def serialize_category(category):
    if category is None:
        return None
    return {
        'id': str(category['_id']),
        'name': category['name'],
    }


def serialize_location(location):
    if location is None:
        return None
    return {
        'id': str(location['_id']),
        'name': location['name'],
    }


def serialize_item(item):
    if item is None:
        return None
    category = categories.find_one({'_id': item.get('category_id')}) if item.get('category_id') else None
    location = locations.find_one({'_id': item.get('location_id')}) if item.get('location_id') else None
    return {
        'id': str(item['_id']),
        'name': item['name'],
        'description': item.get('description', ''),
        'quantity': item.get('quantity', 0),
        'created_at': item['created_at'],
        'category': serialize_category(category),
        'location': serialize_location(location),
    }


def get_category_by_id(category_id):
    if category_id is None:
        return None
    return categories.find_one({'_id': to_object_id(category_id)})


def get_location_by_id(location_id):
    if location_id is None:
        return None
    return locations.find_one({'_id': to_object_id(location_id)})


def get_item_by_id(item_id):
    return items.find_one({'_id': to_object_id(item_id)})


def create_item(data):
    document = {
        'name': data['name'],
        'description': data.get('description', ''),
        'quantity': data.get('quantity', 0),
        'category_id': to_object_id(data.get('category_id')) if data.get('category_id') else None,
        'location_id': to_object_id(data.get('location_id')) if data.get('location_id') else None,
        'created_at': datetime.utcnow(),
    }
    result = items.insert_one(document)
    return items.find_one({'_id': result.inserted_id})


def update_item(item_id, data):
    update_fields = {}
    if 'name' in data:
        update_fields['name'] = data['name']
    if 'description' in data:
        update_fields['description'] = data.get('description', '')
    if 'quantity' in data:
        update_fields['quantity'] = data['quantity']
    if 'category_id' in data:
        update_fields['category_id'] = to_object_id(data.get('category_id')) if data.get('category_id') else None
    if 'location_id' in data:
        update_fields['location_id'] = to_object_id(data.get('location_id')) if data.get('location_id') else None
    items.update_one({'_id': to_object_id(item_id)}, {'$set': update_fields})
    return items.find_one({'_id': to_object_id(item_id)})
