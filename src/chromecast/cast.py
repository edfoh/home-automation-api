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
        self._datetime_played = None
        self._current_media_controller = None

    def play_video(self, url):
        cc = self._getChromecast()
        mc = cc.media_controller
        mc.play_media(url, 'video/mp4')
        mc.block_until_active()
        self._datetime_played = datetime.now()
        self._playing_url = url
        self._current_media_controller = mc
        return mc.status

    def stop(self):
        cc = self._getChromecast()
        self._datetime_played = None
        self._playing_url = None
        self._current_media_controller = None
        cc.quit_app()

    def pause(self):
        if self._current_media_controller != None:
            self._current_media_controller.pause()

    def play(self):
        if self._current_media_controller != None:
            self._current_media_controller.play()

    def play_next(self):
        cc = self._getChromecast()
        mc = cc.media_controller
        if self._is_playing():
            youtubeClient = youtube.YoutubeClient()
            playlistState = youtubeClient.getPlaylistStateForNextVideoInPlaylist()
            print("found playlist state")
            if playlistState != None:
                self.stop()
                print('playing next in playlist')
                self.play_video(playlistState.url)
                playlistState.save()
                return True
            else:
                return False
        else:
            False

    def play_previous(self):
        cc = self._getChromecast()
        mc = cc.media_controller
        if self._is_playing():
            youtubeClient = youtube.YoutubeClient()
            playlistState = youtubeClient.getPlaylistStateForPreviousVideoInPlaylist()
            if playlistState != None:
                self.stop()
                print('playing previous in playlist')
                self.play_video(playlistState.url)
                playlistState.save()
                return True
            else:
                return False
        else:
            False

    def resume(self):
        youtubeClient = youtube.YoutubeClient()
        playlistState = youtubeClient.getCurrentPlaylistState()
        if playlistState != None:
            self.play_video(playlistState.url)
            return True
        else:
            return False

    def playlist_info(self):
        youtubeClient = youtube.YoutubeClient()
        playlistState = youtubeClient.getCurrentPlaylistState()
        return {
            'playlist_id': playlistState.id,
            'playlist_name': playlistState.name,
            'playlist_url': playlistState.url,
            'playlist_position': playlistState.currently_playing_position,
            'playlist_total_results': playlistState.total_results,
            'chromecast_playing_url': self._playing_url,
            'chromecast_datetime_played': self._datetime_played
        }

    def media_status(self):
        if self._current_media_controller != None:
            return self._current_media_controller.status
        else:
            return "Nothing playing"

    def _is_playing(self):
        return self._playing_url != None

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
                    self.play_video(playlistState.url)
                    playlistState.save()
