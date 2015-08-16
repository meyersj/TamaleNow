# Copyright (C) 2015 Jeffrey Meyers
#
# This program is released under the "MIT License".
# Please see the file COPYING in this distribution for
# license terms.


import datetime

from flask import Blueprint, request, jsonify
from webargs import Arg
from webargs.flaskparser import use_args
import geoalchemy2.functions as func


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
    'active':Arg(str, required=True)
}

@mod_api.route("/active", methods=["POST"])
@use_args(active_post_args)
def active_post(args):
    response = dict(**args)
    response["success"] = True
    try:
        record = Active(**args)
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        response["success"] = False
        resonse["exception"] = str(e)
    return jsonify(response)


def query_vendor_status(vendor_id):
    return Active.query.filter_by(vendor_id=vendor_id)\
            .order_by(Active.tstamp.desc())\
            .first() 

active_get_args = {
    'vendor_id':Arg(str, required=True)
}

@mod_api.route('/active', methods=['GET'])
@use_args(active_get_args)
def active_get(args):
    status = query_vendor_status(args["vendor_id"])
    response = dict(**args)
    # found matching record based on input vendor_id
    # return status
    if status:
        response["success"] = True
        response["active"] = status.active
    # no matching vendor id
    else:
        response["success"] = False
        response["msg"] = "no matching vendor_id"
    return jsonify(response)


location_post_args = {
    'vendor_id':Arg(str, required=True),
    'lat':Arg(str, requred=True),
    'lon':Arg(str, requred=True)
}

@mod_api.route("/location", methods=["POST"])
@use_args(location_post_args)
def location_post(args):
    status = query_vendor_status(args["vendor_id"])
    response = dict(vendor_id=args["vendor_id"], success=False)
    if not status:
        response["msg"] = "vendor_id: {0} does not exist".format(args["vendor_id"])
    elif status and not status.active:
        response["msg"] = "vendor_id: {0} is not currently active".\
                format(args["vendor_id"])
    elif status and status.active:
        try:
            location = Locations(**args)
            db.session.add(location)
            db.session.commit()
            response["success"] = True
            response["msg"] = "vendor_id: {0} location updated".\
                    format(args["vendor_id"])
        except Exception as e:
            response["exception"] = str(e)
    return jsonify(response)


def query_vendor_location(vendor_id):
    return db.session.query(
            Locations.vendor_id,
            Locations.tstamp,
            func.ST_X(Locations.geom).label("lon"),
            func.ST_Y(Locations.geom).label("lat"))\
        .filter_by(vendor_id=vendor_id)\
        .order_by(Locations.tstamp.desc())\
        .first()

location_get_args = {
    'vendor_id':Arg(str, required=True)
}

@mod_api.route('/location', methods=['GET'])
@use_args(active_get_args)
def location_get(args):
    status = query_vendor_status(args["vendor_id"])
    response = dict(vendor_id=args["vendor_id"], success=False)
    # vendor does not exists
    if not status:
        response["msg"] = "Error: vendor_id: {0} does not exist".\
                format(args["vendor_id"])
    # vendor is not active
    elif status and not status.active:
        response["msg"] = "vendor_id: {0} is not currently active".\
                format(args["vendor_id"])
    # vendor is active so look up most recent coordinates
    else:
        location = query_vendor_location(args["vendor_id"])
        if location:
            response = dict(
                success=True,
                vendor_id=location.vendor_id,
                tstamp=str(location.tstamp),
                lat=location.lat,
                lon=location.lon
            )
        else:
            response["msg"] = "retrieving coordinates failed"
    return jsonify(response)




