from flask import jsonify, request

from healthcheck import db
from healthcheck.data.models import Projects
from healthcheck.api import api
from healthcheck.api.errors import bad_request


@api.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        query = db.session.query(Projects)
        all_projects = query.all()
        projects_list = []
        for obj in all_projects:
            project = Projects(name=obj.name, email=obj.email,
                               description=obj.description,
                               dependencies=obj.dependencies,
                               id=obj.id)
            projects_list.append(project.to_json())
        get_response = jsonify(projects=projects_list)
        get_response.status_code = 200
        return get_response

    elif request.method == 'POST':
        post_request = request.get_json()
        new_project = Projects(**post_request)
        db.session.add(new_project)
        db.session.commit()
        post_response = jsonify(id=new_project.id, name=new_project.name)
        post_response.status_code = 201
        return post_response


@api.route('/projects/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
def project(project_id):
    if request.method == 'GET':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('project_id not found')
        get_response = jsonify(name=project.name, email=project.email,
                               description=project.description,
                               dependencies=project.dependencies,
                               id=project.id)
        get_response.status_code = 200
        return get_response

    elif request.method == 'DELETE':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('project_id not found')
        db.session.delete(project)
        db.session.commit()
        return '', 204

    elif request.method == 'PUT':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('project_id not found')
        data = request.get_json()
        project.name = data.get('name') or project.name
        project.email = data.get('email') or project.email
        project.dependencies = data.get('dependencies') or project.dependencies
        project.description = data.get('description') or project.description
        db.session.commit()
        put_response = jsonify(project.to_json())
        put_response.status_code = 200
        return put_response
