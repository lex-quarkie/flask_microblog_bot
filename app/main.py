import connexion
from datetime import datetime
import logging

from flask import g, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import (
    JWTManager,
    get_jwt_identity,
)

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .config import Config

logging.basicConfig(level=logging.INFO)


def init_app():
    app = connexion.FlaskApp(
        __name__,
        port=5000,
        specification_dir="../openapi/",
        options={"swagger_ui": True},
    )
    app.add_api("spec.yaml", arguments={"title": "Assignment task"})
    app.app.config.from_object(Config)
    db.init_app(app.app)
    Migrate(app.app, db)
    jwt.init_app(app.app)
    admin.init_app(app.app)

    return app.app


lm = LoginManager()
db = SQLAlchemy(session_options={"autoflush": False})
jwt = JWTManager()
admin = Admin()
ma = Marshmallow()
app = init_app()
lm.init_app(app)

from app import models, views


@lm.user_loader
def load_user(user_id):
    return models.User.get(user_id)


@app.after_request
def after_request(response):
    if g:
        username = g.get("username")
    if get_jwt_identity():
        username = get_jwt_identity().get("username")

    if username:
        user = db.session.query(models.User).filter_by(username=username).first()
        log_entry = models.UserLogEntry(
            user_id=user.id,
            method=request.method,
            url=str(request.url_rule),
            timestamp=datetime.utcnow(),
        )
        db.session.add(log_entry)
        db.session.commit()

    return response


with app.app_context():
    admin.add_views(
        ModelView(models.Post, db.session), ModelView(models.User, db.session)
    )
