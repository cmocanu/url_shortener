# project/test_basic.py


import os
import unittest

import project
import string
import json

class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        self.app = project.app.test_client()
        self.YOUTUBE_LINK1 = 'https://www.youtube.com/watch?v=uAVs0m3Xak4'

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    def add_url(self, url):
        response = self.app.post('/add_url', data=dict(
            url=url,
        ), follow_redirects=True)
        short_url = str(response.data.decode('UTF-8'))
        return short_url
    
    ###############
    #### tests ####
    ###############

    def test_ping(self):
        response = self.app.get('/ping', follow_redirects=True)
        self.assertEqual(response.data.decode('UTF-8'), 'pong')

    def test_post_ping(self):
        response = self.app.post('/ping', data=None, follow_redirects=True)
        self.assertEqual(response.data.decode('UTF-8'), 'postpong') 

    def test_basic_link(self):
        short_url = self.add_url(self.YOUTUBE_LINK1)
        self.assertEqual(len(short_url), 10)
        allowed_characters = string.ascii_lowercase + string.digits
        for char in short_url:
            if char not in allowed_characters:
                self.assertFalse()

    def test_link_visit(self):
        short_url = self.add_url(self.YOUTUBE_LINK1)
        response = self.app.get('/' + short_url, follow_redirects=True)
        url_returned = response.data.decode('UTF-8')
        self.assertEqual(url_returned, self.YOUTUBE_LINK1)

    def test_missing_url(self):
        missing_url = 'addfgty52q'
        response = self.app.get('/' + missing_url, follow_redirects=True)
        self.assertEqual(404, response.status_code)

    def test_visit_info(self):
        short_url = self.add_url(self.YOUTUBE_LINK1)
        self.app.get('/' +  short_url, follow_redirects=True)
        self.app.get('/' +  short_url, follow_redirects=True)
        self.app.get('/' +  short_url, follow_redirects=True)
        response = self.app.get('/info/' +  short_url, follow_redirects=True)
        info = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(info['visits'], 3)

    def test_missing_info(self):
        missing_url = 'addfgty52q'
        response = self.app.get('/info/' + missing_url, follow_redirects=True)
        self.assertEqual(404, response.status_code)

if __name__ == "__main__":
    unittest.main()
