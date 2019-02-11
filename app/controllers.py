from flask import jsonify
from flask import request
from app import app
from sqlalchemy import and_
import json
from sqlalchemy import update
from app.models import Company, User, Skill
from app import db


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/users')
def get_all_users():
    users = User.query.all()
    json_users = []
    for index, user in enumerate(users):
        user_json = dict()
        user_json["name"] = user.name
        user_json["email"] = user.email
        user_json["picture"] = user.picture
        user_json["company"] = user.company
        user_json["phone"] = user.phone
        user_json["latitude"] = user.latitude
        user_json["longitude"] = user.longitude
        user_json["skills"] = []
        sql_get_skills = '''SELECT skills.*
                                FROM skills
                                INNER JOIN users_skills
                                ON skills.skill_id = users_skills.skill_id
                                WHERE users_skills.user_id = {}'''.format(index + 1)

        skills_for_user = db.session.execute(sql_get_skills)
        for skill in skills_for_user:
            skill_json = dict()
            skill_json["name"] = skill.skill_name
            skill_json["rating"] = skill.rating
            user_json["skills"].append(skill_json)
        json_users.append(user_json)
    return jsonify(json_users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return "No user with the specified user_id"
    user_json = dict()
    user_json["name"] = user.name
    user_json["email"] = user.email
    user_json["picture"] = user.picture
    user_json["company"] = user.company
    user_json["phone"] = user.phone
    user_json["latitude"] = user.latitude
    user_json["longitude"] = user.longitude
    user_json["skills"] = []
    sql_get_skills = '''SELECT skills.*
                            FROM skills
                            INNER JOIN users_skills
                            ON skills.skill_id = users_skills.skill_id
                            WHERE users_skills.user_id = {}'''.format(user_id)

    skills_for_user = db.session.execute(sql_get_skills)
    for skill in skills_for_user:
        skill_json = dict()
        skill_json["name"] = skill.skill_name
        skill_json["rating"] = skill.rating
        user_json["skills"].append(skill_json)
    return jsonify(user_json)


@app.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if not request.is_json:
        return "Request is not a json"

    # get the user
    user = User.query.get(user_id)
    content = request.get_json()
    if content["email"] and isinstance(content["email"], str):
        user.email = content["email"]
    if content["name"] and isinstance(content["name"], str):
        user.name = content["name"]
    if content["picture"] and isinstance(content["picture"], str):
        user.picture = content["picture"]
    if content["company"] and isinstance(content["company"], str):
        user.company = content["company"]
    if content["phone"] and isinstance(content["phone"], str):
        user.phone = content["phone"]
    if content["latitude"] and isinstance(content["latitude"], float):
        user.latitude = content["latitude"]
    if content["longitude"] and isinstance(content["longitude"], float):
        user.longitude = content["longitude"]
    if content["skills"]:
        sql_get_skills = '''SELECT skills.*
                            FROM skills
                            INNER JOIN users_skills
                            ON skills.skill_id = users_skills.skill_id
                            WHERE users_skills.user_id = {}'''.format(user_id)
        skills_for_user = db.session.execute(sql_get_skills)
        for skill in content["skills"]:
            name = skill["name"]
            rating = skill["rating"]
            if skills_for_user.query.get(name):
                skills_for_user.query.get(name).rating = rating
            else:
                get_skill = Skill.query.filter_by(and_(Skill.skill_name == name, Skill.rating == rating))
                if get_skill is not None:
                    # insert user_id/skill_id pair to junction table
                else:
                    # create, give id then insert.
    db.session.commit()
    user_json = dict()
    user_json["name"] = user.name
    user_json["email"] = user.email
    user_json["picture"] = user.picture
    user_json["company"] = user.company
    user_json["phone"] = user.phone
    user_json["latitude"] = user.latitude
    user_json["longitude"] = user.longitude
    user_json["skills"] = []
    sql_get_skills = '''SELECT skills.*
                                FROM skills
                                INNER JOIN users_skills
                                ON skills.skill_id = users_skills.skill_id
                                WHERE users_skills.user_id = {}'''.format(user_id)

    skills_for_user = db.session.execute(sql_get_skills)
    for skill in skills_for_user:
        skill_json = dict()
        skill_json["name"] = skill.skill_name
        skill_json["rating"] = skill.rating
        user_json["skills"].append(skill_json)
    return jsonify(user_json)
