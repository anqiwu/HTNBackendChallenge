from flask import jsonify
from flask import request
from sqlalchemy import and_
from app.util import format_user
from app.models import User, SkillWithRating, Skill
from app import db


def post_user(user_id):
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
        skills_for_user = user.skills_with_rating
        for skill in content["skills"]:
            name = skill["name"]
            rating = skill["rating"]
            # the given skill is not one that exists already in the db
            if db.session.query(Skill).filter(Skill.skill_name == name).first() is None:
                # add the skill the the skills table
                new_skill = Skill(name)
                db.session.add(new_skill)
                db.session.commit()
                # add the skill-rating pair to the skills_with_rating table
                new_skill_with_rating = SkillWithRating(name, rating, new_skill.skill_id)
                db.session.add(new_skill_with_rating)
                user.skills_with_rating.append(new_skill_with_rating)
            elif db.session.query(SkillWithRating).filter(
                    and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first() is None:
                # add the skill-rating pair to the skills_with_rating table
                new_skill_with_rating = SkillWithRating(
                    name, rating, db.session.query(Skill).filter(Skill.skill_name == name).first().skill_id)
                db.session.add(new_skill_with_rating)
                user.skills_with_rating.append(new_skill_with_rating)
            elif skills_for_user.filter(SkillWithRating.skill_name == name).first() is None:
                skill_to_add = db.session.query(SkillWithRating).filter(
                    and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first()
                user.skills_with_rating.append(skill_to_add)
            else:
                user_has_skill_name = skills_for_user.filter(SkillWithRating.skill_name == name).first()
                user.skills_with_rating.remove(user_has_skill_name)
                skill_to_add = db.session.query(SkillWithRating).filter(
                    and_(SkillWithRating.skill_name == name, SkillWithRating.rating == rating)).first()
                user.skills_with_rating.append(skill_to_add)
    db.session.commit()
    return jsonify(format_user(user_id))
