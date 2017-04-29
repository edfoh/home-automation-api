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
    'component': lambda tv: tv.sendComponent1(),
    'source': lambda tv: tv.sendSource(),
    'exit': lambda tv: tv.sendExit(),
    'poweroff': lambda tv: tv.powerOff(),
    'volup': lambda tv: tv.volup(),
    'voldown': lambda tv: tv.voldown(),
    'mute': lambda tv: tv.mute(),
    'abckidschannel':  lambda tv: tv.sendAbcKids(),
}

tv_functions_repeats = {
    'volup': lambda tv, times: tv.volupTimes(times),
    'voldown': lambda tv, times: tv.voldownTimes(times),
    'channel': lambda tv, channelNumber: tv.changeChannel(channelNumber),
    'keyup': lambda tv, times: tv.keyUpTimes(times),
    'keydown': lambda tv, times: tv.keyDownTimes(times),
}

@auth.get_password
def get_password(username):
    if username == auth_username:
        return auth_password
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tv/command/<string:command>', methods=['POST'])
@auth.login_required
def run_tv_command(command):
    print('received tv command {}'.format(command))
    with tv.SamsungTv() as samsung_tv:
        if command in tv_functions:
            tv_functions[command](samsung_tv)
            return 'ok'
        else:
            return make_response(jsonify({'error': 'no mapping exists'}), 404)

@app.route('/tv/command/<string:command>/<int:repeats>', methods=['POST'])
@auth.login_required
def run_tv_command_repeats(command, repeats):
    print('received repeat tv command {} with repeats {}'.format(command, repeats))
    with tv.SamsungTv() as samsung_tv:
        if command in tv_functions_repeats:
            tv_functions_repeats[command](samsung_tv, repeats)
            return 'ok'
        else:
            return make_response(jsonify({'error': 'no mapping exists'}), 404)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
