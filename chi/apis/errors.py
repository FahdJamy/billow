from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES as HTC


def make_response(status_code, message=None):
	err_payload = { 'error' : HTC.get(status_code, 'Unknown Error') }
	if message:
		err_payload['message'] = message
	response = jsonify(err_payload)
	response.status_code = status_code
	return response

def bad_request(message):
	return make_response(400, message)