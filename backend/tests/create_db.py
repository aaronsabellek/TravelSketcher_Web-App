import os
from app import db, app

db_path = 'instance/database.db'

if os.path.exists(db_path):
    os.remove(db_path)
    print("Alte Datenbank wurde gelöscht")

# Initialisiere die DB
with app.app_context():
    db.create_all()
    print("Datenbank wurde erstellt!")