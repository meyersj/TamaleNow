#!env/bin/python

# Copyright (C) 2015 Jeffrey Meyers
#
# This program is released under the "MIT License".
# Please see the file COPYING in this distribution for
# license terms.


import unittest
import uuid
import json
import time

from app import app


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    
    #def test_db_config(self):
    #    print app.config["SQLALCHEMY_DATABASE_URI"]
    
    def test_mod_api_index(self):
        res = self.app.get('/api', follow_redirects=True)
        assert res.status_code == 200


class UpdateActiveTests(unittest.TestCase):

    def setUp(self):
        self.vendor = "test_vendor"
        self.app = app.test_client()

    def test_active_post_get(self):
        rv = self.app.post(
            '/api/active',
            data=dict(
                vendor_id=self.vendor,
                active=False
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        assert data["success"] == True
        
        rv = self.app.get(
            '/api/active',
            data=dict(
                vendor_id=self.vendor,
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        assert data["success"] == True
        assert data["active"] == False

        rv = self.app.post(
            '/api/active',
            data=dict(
                vendor_id=self.vendor,
                active=True
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        assert data["success"] == True

        rv = self.app.get(
            '/api/active',
            data=dict(
                vendor_id=self.vendor,
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        assert data["success"] == True
        assert data["active"] == True


class LocationUpdateTests(unittest.TestCase):

    def setUp(self):
        self.vendor = "test_vendor"
        self.app = app.test_client()

    def test_location_post(self):
        rv = self.app.post(
            '/api/active',
            data=dict(
                vendor_id=self.vendor,
                active=True
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        assert data["success"] == True
        
        rv = self.app.post(
            '/api/location',
            data=dict(
                vendor_id=self.vendor,
                tstamp=time.strftime('%Y-%d-%m %H:%M:%S'),
                lat="45.52",
                lon="-122.681944"
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        assert data["success"] == True
     
    def test_location_get(self):
        rv = self.app.get(
            '/api/location',
            data=dict(
                vendor_id=self.vendor,
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        assert data["success"] == True


if __name__ == '__main__':
    unittest.main()





