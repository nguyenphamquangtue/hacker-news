import bcrypt
from database.base import Session
from flask import request, Response
from functools import wraps
from models.user import User


def check_auth(username, password):
    user = Session.query(User).filter(User.username==username).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        return jsonify("Can not logging")
    return user 


def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response(
                "Authentication required.", 401,
            )
        user = Session.query(User).filter(User.username == auth.username).first()
        request.user_id = user.id 
        return func(*args, **kwargs)
    return decorated