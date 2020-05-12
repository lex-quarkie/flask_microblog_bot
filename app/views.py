import bcrypt
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app.main import db
from app.models import (Post, post_schema, posts_schema,
                        User, user_schema)



@jwt_required
def retrieve_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).one()
    result = post_schema.dump(post)
    return result, 200

def create_post(body):
    attrs = body
    post = Post(

    )
    db.session.add(post)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {'error': f'Sqlalchemy Error {repr(ex)}'}, 400


    result = post_schema.dump(post)
    return result, 201


def user_signup(body): # ● user signup
    username = body.get('username', None)
    password = body.get('password', None)


    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(username=username, hash=hashed)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as ex:
        db.session.rollback()
        return {'error': f'Sqlalchemy Error {repr(ex)}'}, 400

    access_token = create_access_token(identity={"username": username})
    return {"access_token": access_token}, 201
# ● post creation

# ● user login
# ● post like
# ● post unlike
# ● analytics about how many likes was made. /api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics aggregated by day.
# ● user activity an endpoint which will show when user was login last time and when he