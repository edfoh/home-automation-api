#!/usr/bin/python

import sys
sys.path.insert(0, './lib')

from flask import Flask

app = Flask("ed-home-automation")

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run()
