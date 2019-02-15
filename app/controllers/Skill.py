from app import db
from app.models.Skill import Skill
from app.models.SkillWithRating import SkillWithRating


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
            all_skill_with_ratings = db.session.query(SkillWithRating).filter(SkillWithRating.skill_id == skill_id)
            frequency = 0
            average_rating = 0
            for one_skill_with_rating in all_skill_with_ratings:
                count = one_skill_with_rating.users.count()
                frequency += count
                average_rating += count * one_skill_with_rating.rating
            average_rating = float("{0:.2f}".format(average_rating / frequency))
            skill_dict["frequency"] = frequency
            skill_dict["average_rating"] = average_rating
            result.append(skill_dict)
        new_result = [x for x in result if x["frequency"] >= min_frequency and x["average_rating"] >= min_rating]

        return new_result
