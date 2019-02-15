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
                # a new skill
                skill_in_db = db.session.query(Skill).filter(Skill.skill_name == name).first()
                if skill_in_db:
                    assoc = db.session.query(UserSkill).filter(
                        and_(UserSkill.user_id == user_id, UserSkill.skill_id == skill_in_db.skill_id)).first()
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

'''
            
            # get all current skills for user_id
            skills_for_user = user.skills_with_rating
            for skill in req_content["skills"]:
                name = skill["name"]
                rating = skill["rating"]

                if skills_for_user.filter(SkillWithRating.skill_name == name).first() is None:

                    # the given skill is not a Skill that exists already in the db
                    if db.session.query(Skill).filter(Skill.skill_name == name).first() is None:
                        print("one", file=sys.stderr)
                        # add the skill the the `skills` table
                        new_skill = Skill(name)
                        db.session.add(new_skill)
                        db.session.commit()
                        # add the skill-rating pair to the `skills_with_rating` table
                        skill_to_add = SkillWithRating(name, rating, new_skill.skill_id)
                        db.session.add(skill_to_add)

                    # the given skill is a existing `Skill`, but the rating is not a rating that exists in the dd
                    elif db.session.query(SkillWithRating).filter(
                            and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first() is None:
                        print("TWO", file=sys.stderr)
                        # add the skill-rating pair to the skills_with_rating table
                        skill_to_add = SkillWithRating(
                            name, rating, db.session.query(Skill).filter(Skill.skill_name == name).first().skill_id)
                        db.session.add(skill_to_add)

                    # the given skill-rating pair is a SkillWithRating row
                    else:
                        print("THREE", file=sys.stderr)
                        skill_to_add = db.session.query(SkillWithRating).filter(
                            and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first()

                else:
                    print("I SHOULD BE HERE", file=sys.stderr)
                    # get the skill with the same name from the list of skills for user_id
                    user_has_skill_name = skills_for_user.filter(SkillWithRating.skill_name == name).first()

                    # remove that skill with the same name as the new skill from the list of skills for user_id
                    user.skills_with_rating.remove(user_has_skill_name)

                    if db.session.query(SkillWithRating).filter(
                            and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first() is None:
                        print("TWO", file=sys.stderr)
                        # add the skill-rating pair to the skills_with_rating table
                        skill_to_add = SkillWithRating(
                            name, rating, db.session.query(Skill).filter(Skill.skill_name == name).first().skill_id)
                        db.session.add(skill_to_add)

                    # get the new skill to add from the skill_with_ratings table
                    skill_to_add = db.session.query(SkillWithRating).filter(
                        and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first()

                user.skills_with_rating.append(skill_to_add)

                if db.session.query(Skill).filter(Skill.skill_name == name).first() is None:
                    print("one", file=sys.stderr)
                    # add the skill the the `skills` table
                    new_skill = Skill(name)
                    db.session.add(new_skill)
                    db.session.commit()
                    # add the skill-rating pair to the `skills_with_rating` table
                    skill_to_add = SkillWithRating(name, rating, new_skill.skill_id)
                    db.session.add(skill_to_add)

                # the given skill is a existing `Skill`, but the rating is not a rating that exists in the dd
                elif db.session.query(SkillWithRating).filter(
                        and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first() is None:
                    print("TWO", file=sys.stderr)
                    # add the skill-rating pair to the skills_with_rating table
                    skill_to_add = SkillWithRating(
                        name, rating, db.session.query(Skill).filter(Skill.skill_name == name).first().skill_id)
                    db.session.add(skill_to_add)

                # the skill_with_rating exists in the db, but is a new skill for the user_id
                elif skills_for_user.filter(SkillWithRating.skill_name == name).first() is None:
                    print("THREE", file=sys.stderr)
                    skill_to_add = db.session.query(SkillWithRating).filter(
                        and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first()

                # the "new" skill is one that the user_id already has, update the rating
                else:
                    print("I SHOULD BE HERE", file=sys.stderr)
                    # get the skill with the same name from the list of skills for user_id
                    user_has_skill_name = skills_for_user.filter(SkillWithRating.skill_name == name).first()

                    # remove that skill with the same name as the new skill from the list of skills for user_id
                    user.skills_with_rating.remove(user_has_skill_name)

                    # get the new skill to add from the skill_with_ratings table
                    skill_to_add = db.session.query(SkillWithRating).filter(
                        and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first()
                    user.skills_with_rating.append(skill_to_add)
        db.session.commit()
'''
