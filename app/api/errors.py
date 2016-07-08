from flask import jsonify


def bad_request(message):
    response = jsonify(message=message)
    response.status_code = 404
    return response


def page_not_found(request):
    if request.accept_mimetypes.accept_json:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response


