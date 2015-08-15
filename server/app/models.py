# Copyright (C) 2015 Jeffrey Meyers

from datetime import datetime

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement

from app import db


def build_geom(lat, lon):
    geom = None
    if lat and lon:
        wkt = 'POINT({0} {1})'.format(lon, lat)
        geom = WKTElement(wkt,srid=4326)
    return geom 

    

class Active(db.Model):
    __tablename__ = 'active'
    vendor_id = db.Column(db.String, primary_key=True)
    active = db.Column(db.Boolean)
    
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class Locations(db.Model):
    __tablename__ = 'locations'
    vendor_id = db.Column(db.String, primary_key=True)
    tstamp = db.Column(db.DateTime, primary_key=True)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    
    def __init__(self, **kwargs):
        self.vendor_id = kwargs["vendor_id"]
        self.tstamp = datetime.strptime(kwargs["tstamp"], '%Y-%d-%m %H:%M:%S')
        self.geom = build_geom(kwargs["lat"], kwargs["lon"]) 

