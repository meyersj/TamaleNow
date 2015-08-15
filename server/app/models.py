# Copyright (C) 2015 Jeffrey Meyers

from geoalchemy2 import Geometry

from app import db


class BaseTable(db.Model):
    
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class Active(BaseTable):
    __tablename__ = 'active'
    vendor_id = db.Column(db.String, primary_key=True)
    active = db.Column(db.Boolean)
    

class Locations(BaseTable):
    __tablename__ = 'locations'
    vendor_id = db.Column(db.String, primary_key=True)
    tstamp = db.Column(db.DateTime)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    
    


