import bcrypt
from datetime import datetime
from connexion import NoContent
from flask import g, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from sqlalchemy.exc import IntegrityError
import sqlalchemy as sa
from app.main import db
from app.models import Like, Post, post_schema, posts_schema, User, UserLogEntry


def login(body):
    username = body.get("username")
    password = body.get("password")

    user = db.session.query(User).filter_by(username=username).one()

    if bcrypt.checkpw(password.encode("utf-8"), user.hash):
        access_token = create_access_token(identity={"username": username})
        g.username = username
        return {"access_token": access_token}, 200

    return {"error": "Bad credentials"}, 400


def user_signup(body):
    username = body.get("username", None)
    user = db.session.query(User).filter_by(username=username).first()
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
    log_entry = UserLogEntry(
        user_id=user.id, method=request.method, url=str(request.url_rule)
    )
    db.session.add(log_entry)
    db.session.commit()
    access_token = create_access_token(identity={"username": username})
    return {"access_token": access_token}, 201


@jwt_required
def retrieve_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()
    result = post_schema.dump(post)
    result["likes_count"] = post.likes()

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
    like = (
        db.session.query(Like).filter_by(user_id=int(user.id), post_id=post.id).first()
    )

    if like:
        db.session.delete(like)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {"error": f"Sqlalchemy Error {repr(ex)}"}, 400
    return NoContent, 200


def analytics(date_from, date_to):
    from pudb import set_trace; set_trace()
    date_rows = dict(
        db.session.query(Like.timestamp, sa.func.count(Like.id))
        .group_by(sa.func.date(Like.timestamp))
        .filter(
            Like.timestamp >= datetime.strptime(date_from, "%Y-%m-%d"),
            Like.timestamp <= datetime.strptime(date_to, "%Y-%m-%d"),
        )
        .all()
    )
    for key in date_rows:
        if isinstance(key, datetime):
            date_rows[key.strftime("%Y-%m-%d").split(" ")[0]] = date_rows.pop(key)
            # ^ dirty hack. SQLite stores DateTime as String, so DateTime=>cast(Date) doesn't work properly
    return date_rows


@jwt_required
def requestlog(user_id):
    latest = (
        db.session.query(UserLogEntry)
        .filter_by(user_id=user_id)
        .order_by(UserLogEntry.timestamp.desc())
        .first()
    )
    login = (
        db.session.query(UserLogEntry)
        .filter(UserLogEntry.url.like("%login%"))
        .filter_by(user_id=user_id)
        .order_by(UserLogEntry.timestamp.desc())
        .first()
    )
    signup = (
        db.session.query(UserLogEntry)
        .filter(UserLogEntry.url.like("%signup%"))
        .filter_by(user_id=user_id)
        .order_by(UserLogEntry.timestamp.desc())
        .first()
    )

    result = {
        "latest_request": latest.timestamp,
        "signup": signup.timestamp,
        "login": login.timestamp,
    }

    return result, 200


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
