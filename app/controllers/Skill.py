from app import db
from app.models.Skill import Skill
from app.models.UserSkill import UserSkill
from sqlalchemy.sql import func


class SkillController:

    @staticmethod
    def get(request):
        min_rating = request.args.get('min_rating', default=0, type=int)
        min_frequency = request.args.get('min_frequency', default=0, type=int)
        result = []
        # Get all skills
        all_skills = db.session.query(Skill).all()
        for skill in all_skills:
            skill_dict = dict()
            skill_dict["name"] = skill.skill_name
            skill_id = skill.skill_id
            all_users_with_skill = db.session.query(UserSkill).filter(UserSkill.skill_id == skill_id)
            rating_sum = db.session.query(func.sum(UserSkill.rating)).filter(UserSkill.skill_id == skill_id).scalar()
            frequency = all_users_with_skill.count()
            average_rating = float("{0:.2f}".format(rating_sum / frequency))
            skill_dict["frequency"] = frequency
            skill_dict["average_rating"] = average_rating
            result.append(skill_dict)
        new_result = [x for x in result if x["frequency"] >= min_frequency and x["average_rating"] >= min_rating]

        return new_result
