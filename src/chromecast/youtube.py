import sys
sys.path.insert(0, './lib')

import subprocess
import httplib2
import os
from datetime import datetime
import chromecast.playlistState as state

from apiclient.discovery import build

from auth.googleOAuth import get_credentials

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = FILE_PATH + "/../credentials/client_secret.json"
AUTH_STORAGE_FILE = FILE_PATH + "/../credentials/google-user-oauth2.json"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# See YouTube API https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/index.html
class YoutubeClient(object):
    def __init__(self):
        credentials = get_credentials(YOUTUBE_READ_WRITE_SSL_SCOPE)
        self.Service = build(API_SERVICE_NAME, API_VERSION,
            http=credentials.authorize(httplib2.Http()))

    def getPlaylist(self):
        playlistResult = self._getPlaylist()
        playlistsItems = playlistResult["items"]
        playlistTitles = list(x["snippet"]["title"] for x in playlistsItems)
        return { 'playlist': playlistTitles }

    def getPlaylistStateForFirstVideoInPlaylist(self, playlistName):
        playlistResult = self._getPlaylist()
        playlists = playlistResult["items"]
        selectedPlaylist = next(item for item in playlists if item["snippet"]["title"] == playlistName)
        if selectedPlaylist == None:
            return None
        else:
            selectedPlaylistId = selectedPlaylist["id"]
            return self._findSelectedPlaylistItem(playlistName, selectedPlaylistId, 0)

    def getPlaylistStateForNextVideoInPlaylist(self):
        playlistState = state.PlaylistState()
        playlistState.restore()
        if playlistState.is_populated():
            print('finding next item in playlist')
            nextPosition = playlistState.currently_playing_position + 1
            if nextPosition == playlistState.total_results:
                print("reached end of playlist")
                return None
            pageToken = playlistState.next_page_token if playlistState.nextItemRequiresPaging() else None
            return self._findSelectedPlaylistItem(playlistState.name, playlistState.id, nextPosition, pageToken)
        else:
            return None

    def getPlaylistStateForPreviousVideoInPlaylist(self):
        playlistState = state.PlaylistState()
        playlistState.restore()
        if playlistState.is_populated():
            print('finding previous item in playlist')
            prevPosition = playlistState.currently_playing_position - 1
            if prevPosition <= 0:
                print("reached start of playlist")
                return None
            pageToken = playlistState.previous_page_token if playlistState.previousItemRequiresPaging() else None
            return self._findSelectedPlaylistItem(playlistState.name, playlistState.id, prevPosition, pageToken)
        else:
            return None

    def getCurrentPlaylistState(self):
        playlistState = state.PlaylistState()
        playlistState.restore()
        if playlistState.is_populated():
            return playlistState
        else:
            return None

    def _findSelectedPlaylistItem(self, playlistName, playlistId, itemPosition, pageToken = None):
        playlistItemsResult = self._getPlaylistItems(playlistId, pageToken)
        playlistItems = playlistItemsResult["items"]
        firstPlaylistItem = playlistItems[itemPosition]
        videoId = firstPlaylistItem["snippet"]["resourceId"]["videoId"]
        videoUrl = str(subprocess.check_output("youtube-dl -g --no-check-certificate -- " + videoId, shell=True))
        return self._createPlaylistState(playlistName, playlistId, playlistItemsResult, firstPlaylistItem, videoUrl)

    def _getPlaylist(self):
        return self.Service.playlists().list(part="snippet", mine=True).execute()

    def _getPlaylistItems(self, id, pageToken = None):
         return self.Service.playlistItems().list(part="snippet", playlistId=id, pageToken=pageToken).execute()

    def _createPlaylistState(self, name, playlistId, playlistItemsResult, selectedPlaylistItem, selectedVideoUrl):
        return state.PlaylistState(
            playlistId,
            name,
            selectedVideoUrl.rstrip(),
            selectedPlaylistItem["snippet"]["position"],
            playlistItemsResult["pageInfo"]["totalResults"],
            playlistItemsResult.get("nextPageToken"),
            playlistItemsResult.get("prevPageToken"))
