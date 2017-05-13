import sys
sys.path.insert(0, './lib')

import os
import pychromecast
from datetime import datetime
import chromecast.youtube as youtube

class Chromecast(object):
    def __init__(self):
        cc_name = os.environ.get("CHROMECAST_NAME")
        self.Chromecast = next(cc for cc in pychromecast.get_chromecasts() if cc.device.friendly_name == cc_name)
        self.Chromecast.media_controller.register_status_listener(self)

    def play(self, url):
        self.Chromecast.wait()
        mc = self.Chromecast.media_controller
        mc.play_media(url, 'video/mp4')
        mc.block_until_active()
        self._datetime_played = datetime.now()
        return mc.status

    def stop(self):
        self.Chromecast.wait()
        self.Chromecast.quit_app()

    def new_media_status(self, status):
        if status.player_state == "IDLE" and status.idle_reason == "FINISHED":
            time_from_last_played = datetime.now() - self._datetime_played
            # to get around the same state being triggered right after a video is triggered
            if (time_from_last_played.total_seconds() > 5):
                print('current casting video finished, playing next in playlist')
                youtubeClient = youtube.YoutubeClient()
                playlistState = youtubeClient.getPlaylistStateForNextVideoInPlaylist()
                if playlistState == None:
                    self.stop()
                    self.tear_down()
                else:
                    self.play(playlistState.url)
                    playlistState.save()
