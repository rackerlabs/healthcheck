from flask import jsonify, request, url_for
from .. import db
from ..models import Projects, Canary
from . import api
from .errors import bad_request


@api.route('/projects/<int:project_id>/canary', methods=['POST'])
def new_canary(project_id):
    if request.method == 'POST':
        post_request = request.get_json()
        new_canary = Canary(**post_request)
        new_canary.project_id = project_id
        canary_project = Projects.query.get(project_id)
        db.session.add(new_canary)
        db.session.commit()
        post_response = jsonify(canary_id=new_canary.id, canary_name=new_canary.name, project=canary_project.name)
        post_response.status_code = 201
        return post_response
        # return jsonify(project_name=project.name), 201, {'Location': url_for('api.project', id=project.id, _external=True)}


@api.route('/projects/<int:project_id>/canary', methods=['GET'])
def get_canaries(project_id):
    project = Projects.query.get(project_id)
    if project is None:
        return bad_request('project_id not found')
    all_canaries = project.canaries.all()
    canary_list = []
    for obj in all_canaries:
        canary = Canary(name=obj.name, description=obj.description, criteria=obj.criteria, data=obj.data, id=obj.id)
        canary_list.append(canary.canary_to_json())
    get_response = jsonify(canaries=canary_list)
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/<int:canary_id>', methods=['GET'])
def get_canary(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None:
        return bad_request('canary_id not found')
    get_response = jsonify(name=canary.name, description=canary.description,
                           data=canary.data, criteria=canary.criteria, id=canary.id)
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/<int:canary_id>', methods=['PUT'])
def edit_canary(project_id, canary_id):
    # #ISSUE WITH TRYING TO CHANGE A FIELD IN THE data OR criteria COLUMN
    project = Projects.query.get(project_id)
    canary = project.get_canary(canary_id)
    data = request.get_json()
    canary.name = data.get('name') or canary.name
    canary.description = data.get('description') or canary.description
    canary.data = data.get('data') or canary.data
    canary.criteria = data.get('criteria') or canary.criteria
    db.session.commit()
    put_response = jsonify(canary.canary_to_json())
    put_response.status_code = 200
    return put_response

    # #OR BY GETTING CANARY DIRECTLY FROM CANARY TABLE??
    # canary = Canary.query.get(canary_id)
    # print canary.canary_to_json()
    # if canary is None:
    #     return bad_request('canary_id not found')
    # data = request.get_json()
    # canary.name = data.get('name') or canary.name
    # canary.description = data.get('description') or canary.description
    # canary.data = data.get('data') or canary.data
    # canary.criteria = data.get('criteria') or canary.criteria
    # db.session.commit()
    # put_response = jsonify(canary.canary_to_json())
    # put_response.status_code = 200
    # return put_response


@api.route('/projects/<int:project_id>/<int:canary_id>', methods=['DELETE'])
def delete_canary(canary_id, project_id):
    # Delete and destroy the link to the project that owns it?
    # possible to reuse id after deletion?
    canary = Canary.query.get(canary_id)
    if canary is None:
        return bad_request('canary_id not found')
    name = canary.name
    db.session.delete(canary)
    db.session.commit()
    response = jsonify(message="Deleted canary '%s' " % name)
    response.status_code = 200
    return response
