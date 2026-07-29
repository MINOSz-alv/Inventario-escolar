"""MongoDB-backed inventory app.

This app uses direct pymongo access for inventory documents. Django ORM models are not used
for inventory data storage; the default Django database remains SQLite for auth and
admin tables.
"""

# Inventory storage is handled in inventory/mongo.py
