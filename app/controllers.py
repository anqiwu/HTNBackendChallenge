from flask import jsonify
from flask import request
from app import app
from sqlalchemy import and_
from app.models import User, Skill
from app import db
import sys


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
    user = db.session.query(User).get(user_id)
    content = request.get_json()
    if "email" in content and isinstance(content["email"], str):
        user.email = content["email"]
    if "name" in content and isinstance(content["name"], str):
        user.name = content["name"]
    if "picture" in content and isinstance(content["picture"], str):
        user.picture = content["picture"]
    if "company" in content and isinstance(content["company"], str):
        user.company = content["company"]
    if "phone" in content and isinstance(content["phone"], str):
        user.phone = content["phone"]
    if "latitude" in content and isinstance(content["latitude"], float):
        user.latitude = content["latitude"]
    if "longitude" in content and isinstance(content["longitude"], float):
        user.longitude = content["longitude"]
    if "skills" in content:
        # get current skills for user_id
        skills_for_user = user.skills
        for skill in content["skills"]:
            name = skill["name"]
            rating = skill["rating"]
            print("]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]", file=sys.stderr)
            print(name, file=sys.stderr)
            print(rating, file=sys.stderr)
            # the given skill is not in the user_id's skills list so
            # 1. check if it already exists in the list of skills
            # 2. if not add skill to "skills" table and update users_skills
            # given skill is a skill that exists already in the db
            if skills_for_user.filter(and_(Skill.skill_name == name, Skill.rating == rating)).first() is None:
                if db.session.query(Skill).filter(and_(Skill.skill_name == name, Skill.rating == rating)).first() is not None:
                    print("THIS IS WORKING OK NOW", file=sys.stderr)
                    skill_to_add = db.session.query(Skill).filter(and_(Skill.skill_name == name, Skill.rating == rating)).first()
                    user.skills.append(skill_to_add)
                else:
                    skill_to_add = Skill(name, rating)
                    db.session.add(skill_to_add)
                    user.skills.append(skill_to_add)
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
