from app.routes.auth import auth_bp
from app.routes.user import user_bp
from app.routes.destination import destination_bp
from app.routes.activity import activity_bp
from app.routes.search import search_bp

def register_blueprints(app):
    """Registers all blueprints from app"""

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(destination_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(search_bp)

