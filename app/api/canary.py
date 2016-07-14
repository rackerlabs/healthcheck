from flask import jsonify, request, url_for
from .. import db
from ..models import Projects, Canary
from . import api
from .errors import bad_request


@api.route('/projects/<int:project_id>/canary', methods=['POST'])
def new_canary(project_id):
    if request.method == 'POST':
        post_request = request.get_json()
        post_request['project_id'] = project_id
        new_canary = Canary(**post_request)
        canary_project = Projects.query.get(project_id)  # is this worth it?
        db.session.add(new_canary)
        db.session.commit()
        post_response = jsonify(id=new_canary.id, name=new_canary.name, status=new_canary.status,
                                project=canary_project.name)
        post_response.status_code = 201
        return post_response


@api.route('/projects/<int:project_id>/canary', methods=['GET'])
def get_canaries(project_id):
    all_canaries = Canary.query.filter_by(project_id=project_id)
    canary_list = []
    for obj in all_canaries:
        if obj.status == "ACTIVE":
            canary_list.append(obj.canary_to_json())
    get_response = jsonify(canaries=canary_list)
    get_response.status_code = 200
    return get_response

@api.route('/projects/<int:project_id>/<int:canary_id>', methods=['GET'])
def get_canary(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    get_response = jsonify(canary.canary_to_json())
    get_response.status_code = 200
    return get_response
    # HEALTH DETAILS OVER TIME COMING SOON...


@api.route('/projects/<int:project_id>/<int:canary_id>', methods=['PUT'])
def edit_canary(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    data = request.get_json()
    canary.name = data.get('name') or canary.name
    canary.description = data.get('description') or canary.description
    canary.data = data.get('data') or canary.data
    canary.criteria = data.get('criteria') or canary.criteria
    db.session.commit()
    put_response = jsonify(canary.canary_to_json())
    put_response.status_code = 200
    return put_response


@api.route('/projects/<int:project_id>/<int:canary_id>', methods=['DELETE'])
def delete_canary(canary_id, project_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('not found')
    name = canary.name
    # db.session.delete(canary)
    canary.status = "DISABLED"
    db.session.commit()
    response = jsonify(message="Deleted canary '%s' " % name)  # CHANGE MESSAGE?
    response.status_code = 200
    return response
