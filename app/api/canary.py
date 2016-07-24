from flask import jsonify, request
from .. import db
from ..models import Canary, Results
from . import api
from .errors import bad_request


@api.route('/projects/<int:project_id>/canary', methods=['POST'])
def new_canary(project_id):
    post_request = request.get_json()
    post_request['project_id'] = project_id
    new_canary = Canary(**post_request)
    db.session.add(new_canary)
    db.session.commit()
    post_response = jsonify(**new_canary.canary_to_json())
    post_response.status_code = 201
    return post_response


@api.route('/projects/<int:project_id>/canary', methods=['GET'])
def get_canaries(project_id):
    all_canaries = Canary.query.filter_by(project_id=project_id).filter_by(status="ACTIVE")
    canary_list = []
    for obj in all_canaries:
        canary_list.append(obj.canary_to_json())
    get_response = jsonify(canaries=canary_list)
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>', methods=['GET'])
def get_canary(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    get_response = jsonify(**canary.canary_to_json())
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>', methods=['PUT'])
def edit_canary(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    data = request.get_json()
    canary.name = data.get('name') or canary.name
    canary.description = data.get('description') or canary.description
    canary.meta_data = data.get('meta_data') or canary.meta_data
    canary.criteria = data.get('criteria') or canary.criteria
    db.session.commit()
    put_response = jsonify(**canary.canary_to_json())
    put_response.status_code = 200
    return put_response


# should be able to merge this with the original PUT API
@api.route('/projects/<int:project_id>/canary/<int:canary_id>/health', methods=['PUT'])
def edit_canary_health(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    data = request.get_json()
    canary.health = data.get('health')
    db.session.commit()
    response = jsonify("canary health updated")
    response.status_code = 200
    return response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>', methods=['DELETE'])
def delete_canary(canary_id, project_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    name = canary.name
    if canary.status == "DISABLED":
        db.session.delete(canary)
        canary_results = Results.query.filter_by(canary_id=canary_id).all()
        for result in canary_results:
            db.session.delete(result)
        db.session.commit()
        return '', 204
    canary.status = "DISABLED"
    db.session.commit()
    response = jsonify("Disabled '%s' " % name)
    response.status_code = 200
    return response
