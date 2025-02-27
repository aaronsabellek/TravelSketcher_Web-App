from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Importiere Flask-Migrate


app = Flask(__name__)
CORS(app)

app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)  # Initialisiere Flask-Migrate mit der App und der DB

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

from routes import home, register, login, dashboard, logout


if __name__ == '__main__':
    db.create_all()  # Initialisiert die DB
    app.run(debug=True)