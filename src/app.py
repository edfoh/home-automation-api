#!/usr/bin/python
import sys
sys.path.insert(0, './lib')

import os
import socket
from flask import Flask

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import tv.samsung as tv

app = Flask("ed-home-automation")

@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    with tv.SamsungTv() as samsung_tv:
        samsung_tv.test()
    app.run()
