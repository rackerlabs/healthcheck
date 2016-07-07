from flask import jsonify, request
from .. import db
from ..models import Projects
from . import api
from .errors import bad_request


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


@api.route('/projects/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
def project(project_id):
    if request.method == 'GET':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('Invalid Input', 'project_id does not exist')
        get_response = jsonify(name=project.name, email=project.email, description=project.description,
                                        dependencies=project.dependencies)
        get_response.status_code = 202
        return get_response

    elif request.method == 'DELETE':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('Invalid Input', 'project_id does not exist')
        return Projects.delete_project(project)

    elif request.method == 'PUT':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('Invalid Input', 'project_id does not exist')
        data = request.get_json()['project']
        try:
            project.name = data.get('name')
        except KeyError:
            pass

        try:
            project.email = data.get('email')
        except KeyError:
            pass

        try:
            project.dependencies = data.get('dependencies')
        except KeyError:
            pass

        try:
            project.description = data.get('description')
        except KeyError:
            pass

        db.session.commit()
        # or do a DB query of the project to be sure the changes are gotten?
        response = jsonify(project=project.to_json())
        response.status_code = 201
        return response

