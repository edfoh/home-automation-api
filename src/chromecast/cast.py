import sys
sys.path.insert(0, './lib')

import os
import pychromecast
from datetime import datetime
import chromecast.youtube as youtube

class Chromecast(object):
    def __init__(self):
        self.ChromeCastName = os.environ.get("CHROMECAST_NAME")
        cc = self._getChromecast()
        cc.media_controller.register_status_listener(self)
        self._playing_url = None

    def play(self, url):
        cc = self._getChromecast()
        mc = cc.media_controller
        mc.play_media(url, 'video/mp4')
        mc.block_until_active()
        self._datetime_played = datetime.now()
        self._playing_url = url
        return mc.status

    def stop(self):
        cc = self._getChromecast()
        self._datetime_played = None
        self._playing_url = None
        cc.quit_app()

    def _getChromecast(self):
        cc = next(cc for cc in pychromecast.get_chromecasts() if cc.device.friendly_name == self.ChromeCastName)
        cc.wait()
        return cc

    def new_media_status(self, status):
        # when video changed from what we played, we nvoid the url
        if status.player_state == "PLAYING" and status.stream_type == "BUFFERED":
            if str(status.content_id) != str(self._playing_url):
                self._playing_url = None
        # video interrupted
        elif status.idle_reason == "INTERRUPTED":
            self._playing_url = None
        # if video has finished play and was the video we played b4, we move to next in playlists
        elif self._playing_url != None and status.content_id != None \
                and str(status.content_id) == str(self._playing_url) \
                and status.player_state == "IDLE" and status.idle_reason == "FINISHED":
            time_from_last_played = datetime.now() - self._datetime_played
            # to get around the same state being triggered right after a video is triggered
            if (time_from_last_played.total_seconds() > 10):
                print('current casting video finished, playing next in playlist')
                youtubeClient = youtube.YoutubeClient()
                playlistState = youtubeClient.getPlaylistStateForNextVideoInPlaylist()
                if playlistState == None:
                    print('nothing to play')
                    self.stop()
                else:
                    print('found next item to play')
                    self.play(playlistState.url)
                    playlistState.save()
