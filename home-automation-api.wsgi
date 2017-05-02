#!/usr/bin/python
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.insert(0, FILE_PATH)
sys.path.insert(0, FILE_PATH + '/lib')

from src.api import app as application
