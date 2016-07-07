from flask import jsonify


def bad_request(title, message):
    response = jsonify({'error': title, 'message': message})
    response.status_code = 400
    return response
