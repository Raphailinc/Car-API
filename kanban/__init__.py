from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from .config import load_config

db = SQLAlchemy()
ma = Marshmallow()


def create_app() -> Flask:
    app = Flask(__name__)
    load_config(app)
    CORS(app)
    db.init_app(app)
    ma.init_app(app)

    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
