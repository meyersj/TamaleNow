# Copyright (C) 2015 Jeffrey Meyers


import datetime

from flask import Blueprint, request, jsonify
from webargs import Arg
from webargs.flaskparser import use_args

from app import app, db
from app.models import Active, Locations


mod_api = Blueprint('api', __name__, url_prefix='/api')


@mod_api.errorhandler(422)
def handle_bad_request(err):
    data = getattr(err, 'data')
    if data: message = data['message']
    else: message = 'Invalid request'
    return jsonify({'error': message }), 422


@mod_api.route('/')
def index():
    return "api module"

active_post_args = {
    'vendor_id':Arg(str, required=True),
    'active':Arg(bool, required=True)
}

@mod_api.route('/active', methods=['POST'])
@use_args(active_post_args)
def active_post(args):
    response = dict(**args)
    #record = Survey(**args)
    #db.session.add(record)
    #db.session.commit()
    #response["success"] = True
    #except Exception as e:
    #response["success"] = False
    #response["error"] = str(e)
    return jsonify(response)

active_get_args = {
    'vendor_id':Arg(str, required=True)
}

@mod_api.route('/active', methods=['GET'])
@use_args(active_get_args)
def active_get(args):
    response = dict(**args)
    return jsonify(response)


