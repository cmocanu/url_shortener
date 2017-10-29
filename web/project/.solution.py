#################
#### imports ####
#################

from os.path import join, isfile

import random
import string
import json
from flask import Flask, render_template, make_response, jsonify, request, session

################
#### config ####
################

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

##############
#### data ####
##############
class UrlInfo(object):
    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url
        self.visits = 0
    
    def visit(self):
        self.visits += 1

    def to_json(self):
        data = {}
        data['url'] = self.url
        data['short_url'] = self.short_url
        data['visits'] = self.visits
        return json.dumps(data)

class UrlDatabase(object):
    def __init__(self):
        self.short_url_mapping = {}
        self.original_url_mapping = {}

    def add_url(self, original_url, short_url):
        info = UrlInfo(original_url, short_url)
        self.original_url_mapping[original_url] = info
        self.short_url_mapping[short_url] = info

    def get_original_url_info(self, url):
        if url in self.original_url_mapping:
            return self.original_url_mapping.get(url)
        return None
    
    def get_short_url_info(self, url):
        if url in self.short_url_mapping:
            return self.short_url_mapping.get(url)
        return None

db = UrlDatabase()

################
#### routes ####
################
@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'GET':
        return 'pong'
    elif request.method == 'POST':
        return 'postpong'

@app.route('/add_url', methods=['POST'])
def add_url():
    original_url = request.form.get('url')
    short_url = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
    db.add_url(original_url, short_url)
    return short_url

@app.route('/<url>', methods=['GET'])
def visit_url(url):
    info = db.get_short_url_info(url)
    if info is not None:
        info.visits += 1
        return info.url
    else:
        return 'URL not found', 404

@app.route('/info/<url>', methods=['GET'])
def get_url_info(url):
    info = db.get_short_url_info(url)
    if info is not None:
        return info.to_json()
    else:
        return 'URL not found', 404
