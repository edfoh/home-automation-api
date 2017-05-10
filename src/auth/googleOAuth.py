import sys
sys.path.insert(0, './lib')

import httplib2
import os

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = FILE_PATH + "/client_secret.json"
AUTH_STORAGE_FILE = FILE_PATH + "/google-user-oauth2.json"

MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

def get_credentials(scope):
    args = argparser.parse_args()
    args.noauth_local_webserver = True
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=scope,
        message=MISSING_CLIENT_SECRETS_MESSAGE)
    flow.params['access_type'] = 'offline'

    storage = Storage(AUTH_STORAGE_FILE)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)
    return credentials
