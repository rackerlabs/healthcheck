from flask import jsonify, request, url_for
from .. import db
from ..models import Projects, Canary, CanaryResults
from . import api
from .errors import bad_request


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/results', methods=['POST'])
def new_result(canary_id, project_id):
    post_request = request.get_json()
    post_request['canary_id'] = canary_id
    new_result = CanaryResults(**post_request)
    db.session.add(new_result)
    db.session.commit()
    post_response = jsonify(**new_result.results_to_json())
    post_response.status_code = 201
    return post_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/results', methods=['GET'])
def get_results(project_id, canary_id):
    all_results = CanaryResults.query.filter_by(canary_id=canary_id)
    result_list = []
    for obj in all_results:
        result_list.append(obj.results_to_json())
    get_response = jsonify(results=result_list)
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/results/<int:result_id>', methods=['GET'])
def get_result(project_id, canary_id, result_id):
    result = CanaryResults.query.get(result_id)
    if result is None or result.canary_id != canary_id:
        return bad_request('result not found')
    get_response = jsonify(**result.results_to_json())
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/results/<int:result_id>', methods=['PUT'])
def edit_result(project_id, canary_id, result_id):
    result = CanaryResults.query.get(result_id)
    if result is None or result.canary_id != canary_id:
        return bad_request('result not found')
    data = request.get_json()
    result.status = data.get('status') or result.status
    result.failure_details = data.get('failure_details') or result.failure_details
    db.session.commit()
    put_response = jsonify(**result.results_to_json())
    put_response.status_code = 200
    return put_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/results/<int:result_id>', methods=['DELETE'])
def delete_result(project_id, canary_id, result_id):
    result = CanaryResults.query.get(result_id)
    if result is None or result.canary_id != canary_id:
        return bad_request('result not found')
    db.session.delete(result)
    db.session.commit()
    return '', 204


# Archive results on delete if canary is disabled
# use route without project_id or use project_id in code
