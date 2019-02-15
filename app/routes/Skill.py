from flask import jsonify
from flask import request
from app import app
from app.controllers.Skill import SkillController


@app.route('/skills', methods=['Get'])
def get():
    get_result = SkillController.get(request)
    return jsonify(get_result)
