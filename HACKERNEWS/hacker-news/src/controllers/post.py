from flask import Blueprint, request, jsonify
from models.user import User
from models.post import Post
from database.base import Session
from helpers.auth import requires_auth


post = Blueprint(__name__, "post")


@post.route('/posts', methods=['GET'])
def get_all_post():
    posts = Session.query(Post).all()
    result = []
    for post in posts:
        result.append(post.to_json())
    return jsonify(result)


@post.route('/posts', methods=['POST'])
@requires_auth
def create_post_by_user_id():
    data = request.get_json()
    post = Post(data['title'], data['body'], request.user_id)
    post.save()
    return jsonify(post.to_json())
