# Copyright (C) 2015 Jeffrey Meyers


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


def get_vendor(vendor_id):
    return Active.query.filter_by(vendor_id=vendor_id).first() 


active_post_args = {
    'vendor_id':Arg(str, required=True),
    'active':Arg(str, required=True)
}


@mod_api.route("/active", methods=["POST"])
@use_args(active_post_args)
def active_post(args):
    record = get_vendor(args["vendor_id"])
    # vendor already exists so update active field
    if record:
        record.active = args["active"]
        response = dict(
            success=True,
            vendor_id=record.vendor_id,
            active=record.active,
            msg="updated existing vendor record"
        )
    # create new record for vendor
    else:
        record = Active(**args)
        db.session.add(record)
        response = dict(
            success=True,
            vendor_id=record.vendor_id,
            active=record.active,
            msg="create new vendor record"
        )
    db.session.commit()
    return jsonify(response)

active_get_args = {
    'vendor_id':Arg(str, required=True)
}

@mod_api.route('/active', methods=['GET'])
@use_args(active_get_args)
def active_get(args):
    record = get_vendor(args["vendor_id"])
    if record:
        response = dict(
            success=True,
            active=record.active,
            vendor_id=record.vendor_id
        )
    else:
        response = dict(
            success=False,
            error="no matching vendor_id"
        )
    return jsonify(response)


location_post_args = {
    'vendor_id':Arg(str, required=True),
    'tstamp':Arg(str, required=True),
    'lat':Arg(float, requred=True),
    'lon':Arg(float, requred=True)
}



@mod_api.route("/location", methods=["POST"])
@use_args(location_post_args)
def location_post(args):
    record = get_vendor(args["vendor_id"])
    response = dict(**args)
    if not record:
        response = dict(
            vendor_id=args["vendor_id"],
            success=False,
            msg="vendor_id: {0} does not exist".format(args["vendor_id"])
        )
    elif not record.active:
        response = dict(
            vendor_id=args["vendor_id"],
            success=False,
            msg="vendor_id: {0} is not currently active".format(args["vendor_id"])
        )
    else:
        location = Locations(**args)
        db.session.add(location)
        db.session.commit()
        response = dict(
            vendor_id=args["vendor_id"],
            success=True,
            msg="vendor_id: {0} location updated".format(args["vendor_id"])
        )
    return jsonify(response)


location_get_args = {
    'vendor_id':Arg(str, required=True)
}

@mod_api.route('/location', methods=['GET'])
@use_args(active_get_args)
def location_get(args):
    response = {}
    record = get_vendor(args["vendor_id"])
    if not record:
        response = dict(
            success=False,
            error="vendor_id: {0} does not exist".format(args["vendor_id"])
        )
    elif not record.active:
        response = dict(
            success=False,
            error="vendor_id: {0} is not currently active".format(args["vendor_id"])
        )
    else:
        response = {}
        location = db.session.query(
                Locations.vendor_id,
                Locations.tstamp,
                func.ST_X(Locations.geom).label("lon"),
                func.ST_Y(Locations.geom).label("lat"))\
            .filter_by(vendor_id=args["vendor_id"])\
            .order_by(Locations.tstamp.desc())\
            .first()
        
        if location:
            response = dict(
                success=True,
                vendor_id=location.vendor_id,
                tstamp=str(location.tstamp),
                lat=location.lat,
                lon=location.lon
            )
        else:
            response = dict(
                success=False,
                msg="getting coordinates failed"
            )
    return jsonify(response)




