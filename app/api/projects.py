from flask import jsonify, request,url_for
from .. import db
from ..models import Projects
from . import api
from .errors import bad_request


@api.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        query = db.session.query(Projects)
        all_projects = query.all()
        projects_list = []
        for obj in all_projects:
            project = Projects(name=obj.name, email=obj.email, description=obj.description, dependencies=obj.dependencies, id=obj.id)
            projects_list.append(project.to_json())
        get_response = jsonify(projects=projects_list)
        get_response.status_code = 200
        return get_response

    elif request.method == 'POST':
        post_request = request.get_json()
        new_project = Projects(**post_request)
        db.session.add(new_project)
        db.session.commit()
        post_response = jsonify(project_id=new_project.id, project_name=new_project.name)
        post_response.status_code = 201
        return post_response
        # return jsonify(project_name=project.name), 201, {'Location': url_for('api.project', id=project.id, _external=True)}


@api.route('/projects/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
def project(project_id):
    if request.method == 'GET':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('project_id not found')
        get_response = jsonify(name=project.name, email=project.email, description=project.description,
                               dependencies=project.dependencies, id=project.id)
        get_response.status_code = 200
        return get_response

    elif request.method == 'DELETE':
        project = Projects.query.get(project_id)
        if project is None:
            return bad_request('project_id not found')
        name = project.name
        db.session.delete(project)
        db.session.commit()
        response = jsonify(message="Deleted project '%s' " % name)
        response.status_code = 200
        return response

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
        # DO A DB QUERY TO CHECK IF EDIT WAS SUCCESSFUL (UNIT TEST TO THE RESCUE???)
        put_response = jsonify(project=project.to_json())
        put_response.status_code = 200
        return put_response

