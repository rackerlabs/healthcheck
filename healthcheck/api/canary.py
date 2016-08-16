from flask import jsonify, request
from sqlalchemy import and_, text
import pygal

from healthcheck import db
from healthcheck.data.models import Canary, Results
from healthcheck.api import api
from healthcheck.api.errors import bad_request
from healthcheck.worker.tasks import process_trend


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/trend',
           methods=['GET'])
def get_trend(project_id, canary_id):
    interval = request.args.get('interval')
    resolution = request.args.get('resolution')
    threshold = request.args.get('threshold')
    query_string = text("CURRENT_TIMESTAMP AT TIME ZONE 'UTC' - "
                        "INTERVAL '{}'".format(interval))
    results = Results.query.filter(and_(Results.canary_id == canary_id,
                                        Results.created_at >= query_string))
    results_list = []
    for result in results:
        results_list.append(result.results_to_json())
    analysis_call = process_trend.delay(resolution=resolution,
                                        threshold=threshold,
                                        interval=interval,
                                        results_list=results_list)
    results_list, values = analysis_call.wait()
    labels = format_datetime(values=values, resolution=resolution)
    line = pygal.Line()
    line.title = "Canary Trend over {interval}".format(interval=interval)
    line.x_labels = labels
    line.add("status", [1 if x == "green" else 0 for x in results_list])
    return line.render()


def format_datetime(values, resolution):
    value = resolution.split()
    format_values = []
    if value[1] == "days":
        for timee in values:
            n_time = timee[5:16]
            format_values.append(n_time)
        return format_values
    elif value[1] == "hours":
        for timee in values:
            n_time = timee[5:16]
            format_values.append(n_time)
        return format_values


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
    all_canaries = Canary.query.filter_by(project_id=project_id). \
        filter_by(status="ACTIVE")
    canary_list = []
    for obj in all_canaries:
        canary_list.append(obj.canary_to_json())
    get_response = jsonify(canaries=canary_list)
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>',
           methods=['GET'])
def get_canary(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    get_response = jsonify(**canary.canary_to_json())
    get_response.status_code = 200
    return get_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>',
           methods=['PUT'])
def edit_canary(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    data = request.get_json()
    canary.name = data.get('name') or canary.name
    canary.description = data.get('description') or canary.description
    canary.meta_data = data.get('meta_data') or canary.meta_data
    canary.criteria = data.get('criteria') or canary.criteria
    canary.health = data.get('health') or canary.health
    db.session.commit()
    put_response = jsonify(**canary.canary_to_json())
    put_response.status_code = 200
    return put_response


@api.route('/projects/<int:project_id>/canary/<int:canary_id>',
           methods=['DELETE'])
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
