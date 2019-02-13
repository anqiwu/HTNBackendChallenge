from flask import jsonify
from flask import request
from app import app
from app.util import format_user
from app.bll import post_user
from app.models import User


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    json_users = []
    for index, user in enumerate(users):
        json_users.append(format_user(index + 1))
    return jsonify(json_users)


@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def user_by_id(user_id):
    if request.method == 'GET':
        return jsonify(format_user(user_id))

    if not request.is_json:
        return "Request is not a json"

    return post_user(user_id)
