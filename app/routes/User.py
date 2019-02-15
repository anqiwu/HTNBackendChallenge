from flask import jsonify
from flask import request
from app import app
from app.controllers.User import UserController
from app.models.User import User


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    all_users = []
    for user in users:
        all_users.append(UserController.get(user.user_id))
    return jsonify(all_users)


@app.route('/users/<int:user_id>', methods=['GET', 'PUT'])
def user_by_id(user_id):
    if request.method == 'GET':
        return jsonify(UserController.get(user_id))

    if not request.is_json:
        return "Request is not a json"

    return jsonify(UserController.put(user_id))
