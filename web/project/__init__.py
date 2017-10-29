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

################
#### routes ####
################
@app.route('/ping', methods=['GET'])
def ping():
    if request.method == 'GET':
        return 'pong'
