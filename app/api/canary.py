from flask import jsonify, request, render_template
from .. import db
from ..models import Canary, Results
from . import api
from .errors import bad_request
from app.worker.tasks import process_trend
from celery import shared_task


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/trend', methods=['GET'])
def get_trend(project_id, canary_id):
    results = [{u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 19:08:38 GMT', u'failure_details': u'', u'id': 1},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 19:38:38 GMT', u'failure_details': u'', u'id': 2},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 20:09:38 GMT', u'failure_details': u'', u'id': 3},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 20:48:38 GMT', u'failure_details': u'', u'id': 4},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 21:10:38 GMT', u'failure_details': u'', u'id': 5},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 21:50:38 GMT', u'failure_details': u'', u'id': 6},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 22:09:38 GMT', u'failure_details': u'', u'id': 7},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 22:38:38 GMT', u'failure_details': u'', u'id': 8},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 23:09:38 GMT', u'failure_details': u'', u'id': 9},
               {u'status': u'pass', u'created_at': u'Tue, 26 Jul 2016 23:40:38 GMT', u'failure_details': u'',
                u'id': 10},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 00:09:38 GMT', u'failure_details': u'',
                u'id': 11},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 00:15:38 GMT', u'failure_details': u'',
                u'id': 12},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 01:09:38 GMT', u'failure_details': u'',
                u'id': 13},
               {u'status': u'fail', u'created_at': u'Tue, 27 Jul 2016 01:50:38 GMT', u'failure_details': u'',
                u'id': 14},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 02:22:38 GMT', u'failure_details': u'',
                u'id': 15},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 02:50:38 GMT', u'failure_details': u'',
                u'id': 16},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 03:21:38 GMT', u'failure_details': u'',
                u'id': 17},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 03:50:38 GMT', u'failure_details': u'',
                u'id': 18},
               {u'status': u'pass', u'created_at': u'Tue, 27 Jul 2016 04:09:38 GMT', u'failure_details': u'',
                u'id': 19},
               {u'status': u'fail', u'created_at': u'Tue, 27 Jul 2016 04:20:38 GMT', u'failure_details': u'', u'id': 20}

               ]

    interval = request.args.get('interval')
    resolution = request.args.get('resolution')
    threshold = request.args.get('threshold')
    process_trend.delay(project_id=project_id, canary_id=canary_id, interval=interval, resolution=resolution,
                        threshold=threshold, results=results)
    return jsonify(msg="trending done")


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
    canary.health = data.get('health') or canary.health
    db.session.commit()
    put_response = jsonify(**canary.canary_to_json())
    put_response.status_code = 200
    return put_response


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
