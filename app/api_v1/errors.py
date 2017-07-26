from flask import jsonify,make_response
from . import api


def bad_request(message):
    return make_response(jsonify({'error':'bad request','message':message}),400)


def unauthorized(message):
    return make_response(jsonify({'error':'unauthorized','message':message}),401)


def forbidden(message):
    return make_response(jsonify({'error':'forbidden','message':message}),403)

def not_found(message):
    return make_response(jsonify({'error':'not found','message':message}),404)
    
