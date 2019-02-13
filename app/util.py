from app.models import User
from app import db


def format_user(user_id):
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
    sql_get_skills = '''SELECT skills_with_rating.*
                                    FROM skills_with_rating
                                    INNER JOIN users_skills
                                    ON skills_with_rating.skill_with_rating_id = users_skills.skill_with_rating_id
                                    WHERE users_skills.user_id = {}'''.format(user_id)

    skills_for_user = db.session.execute(sql_get_skills)
    for skill in skills_for_user:
        skill_json = dict()
        skill_json["name"] = skill.skill_name
        skill_json["rating"] = skill.rating
        user_json["skills"].append(skill_json)
    return user_json
