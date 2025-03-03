from app import db, app

# Initialisiere die DB
with app.app_context():
    db.create_all()
    print("Datenbank wurde erstellt!")