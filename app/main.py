import connexion
import logging

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .config import Config

logging.basicConfig(level=logging.INFO)

def init_app():
    app = connexion.FlaskApp(__name__, port=5000, specification_dir="../openapi/", options={'swagger_ui': True})
    app.add_api("spec.yaml", arguments={"title": "Assignment task"})
    app.app.config.from_object(Config)
    db.init_app(app.app)
    Migrate(app.app, db)
    jwt.init_app(app.app)
    admin.init_app(app.app)

    return app.app

db = SQLAlchemy(session_options={"autoflush": False})
jwt = JWTManager()
admin = Admin()
ma = Marshmallow()
app = init_app()

from app import models, views
with app.app_context():
    admin.add_views(ModelView(models.Post, db.session),
                    ModelView(models.User, db.session))






