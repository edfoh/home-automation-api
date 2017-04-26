#!/usr/bin/python
import sys
sys.path.insert(0, './lib')

import os
import socket
from datetime import timedelta
from flask import Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import tv.samsung as tv

auth = HTTPBasicAuth()
auth_username = os.environ.get("USERNAME")
auth_password = os.environ.get("PASSWORD")

app = Flask("ed-home-automation")
app.permanent_session_lifetime = timedelta(seconds=15)

tv_functions = {
    'hdmi': lambda tv: tv.sendHdmi(),
    'tv': lambda tv: tv.sendTv(),
    'poweroff': lambda tv: tv.powerOff()
}

@auth.get_password
def get_password(username):
    if username == auth_username:
        return auth_username
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tv/command/<string:command>', methods=['POST'])
@auth.login_required
def change_tv_source(command):
    print('received tv command {}'.format(command))
    with tv.SamsungTv() as samsung_tv:
        if command in tv_functions:
            tv_functions[command](samsung_tv)
            return 'ok'
        else:
            return make_response(jsonify({'error': 'no mapping exists'}), 404)

if __name__ == '__main__':
    app.run()
