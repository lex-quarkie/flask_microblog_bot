import bcrypt
from connexion import NoContent

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from sqlalchemy.exc import IntegrityError

from app.main import db
from app.models import Like, Post, post_schema, posts_schema, User


def login(body):
    username = body.get("username")
    password = body.get("password")

    user = db.session.query(User).filter_by(username=username).one()

    if bcrypt.checkpw(password.encode("utf-8"), user.hash):
        access_token = create_access_token(identity={"username": username})
        return {"access_token": access_token}, 200

    return {"error": "Bad credentials"}, 400


def user_signup(body):
    username = body.get("username", None)
    user = db.session.query(User).filter_by(username=username).one()
    if user:
        return {"error": f"User with username: {username} already exists"}, 400
    password = body.get("password", None)

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user = User(username=username, hash=hashed)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {"error": f"Sqlalchemy Error {repr(ex)}"}, 400

    access_token = create_access_token(identity={"username": username})
    return {"access_token": access_token}, 201


@jwt_required
def retrieve_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()
    result = post_schema.dump(post)
    return result, 200


@jwt_required
def retrieve_all_posts(post_id):
    posts = db.session.query(Post).all()
    result = posts_schema.dump(posts)
    return result, 200


@jwt_required
def like_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()
    current_user = get_jwt_identity()
    user = db.session.query(User).filter_by(username=current_user["username"]).one()
    like = Like(user_id=int(user.id), post_id=post.id)
    db.session.add(like)

    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {"error": f"Sqlalchemy Error {repr(ex)}"}, 400
    return NoContent, 201


@jwt_required
def unlike_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()

    current_user = get_jwt_identity()
    user = db.session.query(User).filter_by(username=current_user["username"]).one()
    like = db.session.query(Like).filter_by(user_id=int(user.id), post_id=post.id).one()

    db.session.delete(like)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {"error": f"Sqlalchemy Error {repr(ex)}"}, 400
    return NoContent, 200


# ● post creation

# ● analytics about how many likes was made. /api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics aggregated by day.
# ● user activity an endpoint which will show when user was login last time and when he


@jwt_required
def create_post(body):
    current_user = get_jwt_identity()
    user = db.session.query(User).filter_by(username=current_user["username"]).one()
    post = Post(body=body.get("body"), user_id=user.id)

    db.session.add(post)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {"error": f"Sqlalchemy Error {repr(ex)}"}, 400

    result = post_schema.dump(post)
    return result, 201
