import bcrypt
from flask import Blueprint, request, jsonify
from models.user import User
from models.post import Post
from sqlalchemy.orm import Session


user = Blueprint(__name__, "user")


@user.route('/users', methods=['GET'])
def get_all_users():
    users = Session.query(User).all()
    result = []
    for user in users:
        result.append(user.to_json())
    return jsonify(result)


@user.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(data['username'], data['password'])
    user.save()
    return jsonify(user.to_json())


@user.route('/users/login', methods=['POST'])
def log_in():
    data = request.get_json()
    user = Session.query(User).filter(User.username == data['username']).first()
    if not user:
        return jsonify("Can not logging")
    if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
        return jsonify("Password not correct")
    return jsonify(user.to_json())


