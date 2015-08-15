# Copyright (C) 2015 Jeffrey Meyers

from geoalchemy2 import Geometry

from app import db


    

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
    tstamp = db.Column(db.DateTime)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
   


