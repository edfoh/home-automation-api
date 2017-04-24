#!/usr/bin/python
import sys
sys.path.insert(0, './lib')

import os
import socket
from datetime import timedelta
from flask import Flask, jsonify, make_response

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import tv.samsung as tv

app = Flask("ed-home-automation")
app.permanent_session_lifetime = timedelta(seconds=15)

tv_functions = {
    'hdmi': lambda tv: tv.sendHdmi(),
    'tv': lambda tv: tv.sendTv(),
    'poweron': lambda tv: tv.powerOn(),
    'poweroff': lambda tv: tv.powerOff()
}

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tv/command/<string:command>', methods=['POST'])
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
