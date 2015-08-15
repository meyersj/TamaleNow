#!env/bin/python

# Copyright (C) 2015 Jeffrey Meyers


import unittest
import uuid
import json

from app import app


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    #def test_mod_api_index(self):
    #    res = self.app.get('/api', follow_redirects=True)
    #    assert res.status_code == 200


class UploadRecordTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    #def test_upload_empty(self):
    #    rv = self.app.post(
    #        '/api/upload/record', {}, follow_redirects=True
    #    )
    #    data = json.loads(rv.data)
    #    assert "error" in data, "missing required params"
    #    assert rv.status_code == 422

    #def test_upload_basic_no_questions(self):
    #    rv = self.app.post(
    #        '/api/upload/record',
    #        data=dict(
    #    	    tstamp="2000-01-01 12:12:12",
	#	        username="testuser",
    #            route="TEST_NONE",
    #            uuid= uuid.uuid4()
    #        ),
    #        follow_redirects=True
    #    )
    #   assert rv.status_code == 200



if __name__ == '__main__':
    unittest.main()





