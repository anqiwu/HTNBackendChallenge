from app import db
from app.models.Skill import Skill
from app.models.UserSkill import UserSkill
from sqlalchemy.sql import func


class SkillController:

    @staticmethod
    def get(request):
        min_rating = request.args.get('min_rating', default=0, type=int)
        min_frequency = request.args.get('min_frequency', default=0, type=int)
        skills_stats = []

        # Get all skills
        all_skills = db.session.query(Skill).all()
        for skill in all_skills:
            skill_dict = dict()
            skill_id = skill.skill_id
            skill_dict["name"] = skill.skill_name

            # look in UserSkill and get all rows where UserSkill.skill_id == skill_id), i.e, get all users for skill_id
            all_users_with_skill = db.session.query(UserSkill).filter(UserSkill.skill_id == skill_id)

            # sum the ratings
            rating_sum = db.session.query(func.sum(UserSkill.rating)).filter(UserSkill.skill_id == skill_id).scalar()

            # get the number of users with the given skill
            frequency = all_users_with_skill.count()

            # calculate the average rating and truncate to a 2 decimal precision float
            average_rating = float("{0:.2f}".format(rating_sum / frequency))
            skill_dict["frequency"] = frequency
            skill_dict["average_rating"] = average_rating
            skills_stats.append(skill_dict)

        # filter out the skills that do not match the request params
        stats_to_keep = [x for x in skills_stats if x["frequency"] >= min_frequency and x["average_rating"] >= min_rating]

        return stats_to_keep
