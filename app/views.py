from flask import jsonify

from app.main import db
from app.models import Post


def retrieve_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()

    return (post), 200
