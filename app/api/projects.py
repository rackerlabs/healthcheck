from flask import jsonify, request
from .. import db
from ..models import Projects
from . import api

@api.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        projects_list = Projects.get_projects()
        return jsonify(projects=projects_list)
    elif request.method == 'POST':
        post = request.get_json()
        post_request = post['project']
        project = Projects.new_project(post_request)
        post_response = jsonify(project_id=project.id, project_name=project.name)
        post_response.status_code = 201
        return post_response
