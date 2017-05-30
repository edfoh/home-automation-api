import sys
sys.path.insert(0, './lib')

import os
import pickle

class PlaylistState(object):
    def __init__(self, id = "", name = "", url = "", position = 0, total_results = 0, next_page_token = "", previous_page_token = ""):
        self._id = id
        self._name = name
        self._url = url
        self._playlist_position = position
        self._total_results = total_results
        self._next_page_token = next_page_token
        self._previous_page_token = previous_page_token

    @property
    def name(self):
        return self._name

    @property
    def currently_playing_position(self):
        return self._playlist_position

    @property
    def id(self):
        return self._id

    @property
    def url(self):
        return self._url

    @property
    def total_results(self):
        return self._total_results

    @property
    def next_page_token(self):
        return self._next_page_token

    @property
    def previous_page_token(self):
        return self._previous_page_token

    def is_populated(self):
        return self._name != None or self._name != ""

    def nextItemRequiresPaging(self):
        currentIndex = int(self._playlist_position / 5)
        newIndex = int(self._playlist_position + 1 / 5)
        return currentIndex != newIndex

    def previousItemRequiresPaging(self):
        currentIndex = int(self._playlist_position / 5)
        newIndex = int(self._playlist_position - 1 / 5)
        return currentIndex != newIndex

    def save(self):
        with open('playlist_state.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def restore(self):
        if os.path.isfile('playlist_state.pkl'):
            print("restore playlist state from disk")
            with open('playlist_state.pkl', 'rb') as input:
                restored = pickle.load(input)
                self._id = restored.id
                self._name = restored.name
                self._url = restored.url.rstrip()
                self._playlist_position = restored.currently_playing_position
                self._total_results = restored.total_results
                self._next_page_token = restored.next_page_token
                self._previous_page_token = restored.previous_page_token
