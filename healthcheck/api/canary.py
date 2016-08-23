from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy import and_, text
import pygal
from healthcheck import db
from healthcheck.data.models import Canary, Results
from healthcheck.api import api
from healthcheck.api.errors import bad_request
from healthcheck.worker.tasks import process_trend
from pygal.style import Style

trend_style = Style(
    background='transparent',
    plot_background='transparent',
    colors=('#808080', '#0000FF'))

history_style = Style(
    background='transparent',
    plot_background='transparent',
    colors=('#808080', '#0000FF'))

node = {'r': 4}
red_style = 'fill: red'
green_style = 'fill: green'


@api.route('/projects/<int:project_id>/canary/<int:canary_id>/history',
           methods=['GET'])
def get_history(project_id, canary_id):
    canary = Canary.query.get(canary_id)
    if canary is None or canary.project_id != project_id:
        return bad_request('canary not found')
    history = canary.history
    line = pygal.Line(x_label_rotation=60, style=history_style)
    time_list = []
    health_list = []
    for key, value in sorted(history.items()):
        time_list.append(key)
        health_list.append(value)

    line.title = "Canary History Graph"
    line.x_labels = [
        datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f").strftime(
            '%d, %b %Y at %I:%M:%S')
        for dt in time_list]
    line.y_labels = [
        {
            'value': 3,
            'label': ''
        },
        {
            'value': 2,
            'label': 'Green'
        },
        {
            'value': 1,
            'label': 'Red'
        },
        {
            'value': 0,
            'label': ''
        }
    ]

    line.add('Health', [{'value': 2, 'node': node, 'style': green_style}
                        if x == "GREEN"
                        else
                        {'value': 1, 'node': node, 'style': red_style}
                        for x in health_list])

    return line.render()


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

    start_time = datetime.utcnow()
    analysis_call = process_trend.delay(resolution=resolution,
                                        threshold=threshold,
                                        interval=interval,
                                        start_time=start_time,
                                        results_list=results_list)
    results_list, values = analysis_call.wait()
    labels, res_hour = format_datetime(values, resolution)
    threshold_list = []
    for i in range(len(results_list)):
        threshold_list.append(int(threshold))

    line = pygal.Line(width=1000, height=800, style=trend_style,
                      x_label_rotation=60, range=(0, 100),
                      x_title='Resolution Hour: {}'.
                      format(res_hour))
    line.title = "Canary Trend over {interval}".format(interval=interval)
    line.x_labels = labels
    line.add('Status', [
        {'value': x, 'node': node, 'style': green_style}
        if x >= int(threshold) else
        {'value': x, 'node': node, 'style': red_style}
        for x in results_list
        ])
    line.add("threshold", threshold_list, show_dots=False,
             stroke_style={'width': 2})
    return line.render()


def format_datetime(values, resolution):
    res_value = resolution.split()
    format_values = []
    offset = timedelta(days=int(res_value[0]))
    start = values[0][11:19]
    before_res = datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S.%f") - offset
    after_res = datetime.strptime(values[len(values) - 1],
                                  "%Y-%m-%d %H:%M:%S.%f") + offset
    first_val = ""
    if res_value[1] == "days":
        for index, timee in enumerate(values):
            if index == 0:
                n_time = timee[5:10]
                before = before_res.strftime('%m-%d')
                format_values.append(before + ' to ' + n_time)
                first_val = n_time
            elif index == len(values) - 1:
                n_time = timee[5:10]
                after = after_res.strftime('%m-%d')
                format_values.append(n_time + ' to ' + after)
            else:
                n_time = timee[5:10]
                format_values.append(first_val + ' to ' + n_time)
                first_val = n_time
        return format_values, start
    for timee in values:
        n_time = timee[5:16]
        format_values.append(n_time)
    return format_values, start


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
    canary.update_health(new_health=data.get('health'))
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
