import sys
sys.path.insert(0, './lib')

import os
import pychromecast
import chromecast.youtube as youtube

class Chromecast(object):
    def __init__(self):
        cc_name = os.environ.get("CHROMECAST_NAME")
        self.Chromecast = next(cc for cc in pychromecast.get_chromecasts() if cc.device.friendly_name == cc_name)
        self.Chromecast.media_controller.register_status_listener(self)
        self._processing_update = False

    def play(self, url):
        self.Chromecast.wait()
        mc = self.Chromecast.media_controller
        mc.play_media(url, 'video/mp4')
        mc.block_until_active()
        return mc.status

    def stop(self):
        self.Chromecast.wait()
        self.Chromecast.quit_app()

    def new_media_status(self, status):
        if status.player_state == "IDLE" and status.idle_reason == "FINISHED" and not self._processing_update:
            print('current casting video finished, playing next in playlist')
            self._processing_update = True
            try:
                youtubeClient = youtube.YoutubeClient()
                playlistState = youtubeClient.getPlaylistStateForNextVideoInPlaylist()
                if playlistState == None:
                    self.stop()
                else:
                    self.play(playlistState.url)
                    playlistState.save()
            finally:
                self._processing_update = False
