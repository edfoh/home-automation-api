import sys
sys.path.insert(0, './lib')

import httplib2
import os

from apiclient.discovery import build

from auth.google import get_credentials

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = FILE_PATH + "/../credentials/client_secret.json"
AUTH_STORAGE_FILE = FILE_PATH + "/../credentials/google-user-oauth2.json"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

class YoutubeClient(object):
    def __init__(self):
        credentials = get_credentials(YOUTUBE_READ_WRITE_SSL_SCOPE)
        self.Service = build(API_SERVICE_NAME, API_VERSION,
            http=credentials.authorize(httplib2.Http()))

    def getPlaylist(self):
        result = self.Service.playlists().list(part="snippet",mine=True).execute()
        items = list(x["snippet"]["title"] for x in result["items"])
        return { 'playlist': items }
