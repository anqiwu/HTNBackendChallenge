from flask import request
from sqlalchemy import and_
from app.models.User import User
from app.models.Skill import Skill
from app.models.UserSkill import UserSkill
from app import db
import sys


class UserController:

    @staticmethod
    def get(user_id):
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
        user_skills = user.skills
        for assoc in user_skills:
            skill_json = dict()
            skill_json["name"] = assoc.skill.skill_name
            skill_json["rating"] = assoc.rating
            user_json["skills"].append(skill_json)
        return user_json

    @staticmethod
    def put(user_id):
        user = db.session.query(User).get(user_id)
        req_content = request.get_json()

        if "email" in req_content and isinstance(req_content["email"], str):
            user.email = req_content["email"]

        if "name" in req_content and isinstance(req_content["name"], str):
            user.name = req_content["name"]

        if "picture" in req_content and isinstance(req_content["picture"], str):
            user.picture = req_content["picture"]

        if "company" in req_content and isinstance(req_content["company"], str):
            user.company = req_content["company"]

        if "phone" in req_content and isinstance(req_content["phone"], str):
            user.phone = req_content["phone"]

        if "latitude" in req_content and isinstance(req_content["latitude"], float):
            user.latitude = req_content["latitude"]

        if "longitude" in req_content and isinstance(req_content["longitude"], float):
            user.longitude = req_content["longitude"]

        if "skills" in req_content:
            for skill in req_content["skills"]:
                name = skill["name"]
                rating = skill["rating"]
                if not isinstance(name, str) or not isinstance(rating, int):
                    continue
                # try to get the skill from the db
                skill_in_db = db.session.query(Skill).filter(Skill.skill_name == name).first()

                # if skill is in db, try to get the UserSkill row associated with the skill_id and user_id
                if skill_in_db:
                    assoc = db.session.query(UserSkill).filter(
                        and_(UserSkill.user_id == user_id, UserSkill.skill_id == skill_in_db.skill_id)).first()

                # skill is a brand new skill that does not exists in the db
                if skill_in_db is None:
                    print("one", file=sys.stderr)
                    # add the skill the the `skills` table
                    new_skill = Skill(name)
                    user_skill = UserSkill(rating=rating)
                    user_skill.user = db.session.query(User).filter(User.user_id == user_id).first()
                    new_skill.users.append(user_skill)

                # skill in db that the the user don't have
                elif assoc is None:
                    print("two", file=sys.stderr)
                    skill = db.session.query(Skill).filter(Skill.skill_name == name).first()
                    user_skill = UserSkill(rating=rating)
                    user_skill.user = db.session.query(User).filter(User.user_id == user_id).first()
                    skill.users.append(user_skill)

                # skill in db that user have, need to update:
                else:
                    print("three", file=sys.stderr)
                    assoc.rating = rating

        db.session.commit()
        return UserController.get(user_id)
