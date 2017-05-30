#!/usr/bin/python
import sys
sys.path.insert(0, './lib')

import os
import socket
from datetime import timedelta
from flask import Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import tv.samsung as tv
import chromecast.youtube as youtube
import chromecast.cast as cast
import chromecast.playlistState as state

auth = HTTPBasicAuth()
auth_username = os.environ.get("USERNAME")
auth_password = os.environ.get("PASSWORD")

chromecast = cast.Chromecast()

app = Flask("ed-home-automation")
app.permanent_session_lifetime = timedelta(seconds=60)

tv_functions = {
    'hdmi': lambda tv: tv.sendHdmi(),
    'tv': lambda tv: tv.sendTv(),
    'component': lambda tv: tv.sendComponent1(),
    'source': lambda tv: tv.sendSource(),
    'exit': lambda tv: tv.sendExit(),
    'poweroff': lambda tv: tv.powerOff(),
    'volup': lambda tv: tv.volup(),
    'voldown': lambda tv: tv.voldown(),
    'mute': lambda tv: tv.mute(),
    'abckidschannel':  lambda tv: tv.sendAbcKids(),
}

tv_functions_repeats = {
    'volup': lambda tv, times: tv.volupTimes(times),
    'voldown': lambda tv, times: tv.voldownTimes(times),
    'channel': lambda tv, channelNumber: tv.changeChannel(channelNumber),
    'keyup': lambda tv, times: tv.keyUpTimes(times),
    'keydown': lambda tv, times: tv.keyDownTimes(times),
}

@auth.get_password
def get_password(username):
    if username == auth_username:
        return auth_password
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tv/command/<string:command>', methods=['POST'])
@auth.login_required
def run_tv_command(command):
    print('received tv command {}'.format(command))
    with tv.SamsungTv() as samsung_tv:
        if command in tv_functions:
            tv_functions[command](samsung_tv)
            return 'ok'
        else:
            return make_response(jsonify({'error': 'no mapping exists'}), 404)

@app.route('/tv/command/<string:command>/<int:repeats>', methods=['POST'])
@auth.login_required
def run_tv_command_repeats(command, repeats):
    print('received repeat tv command {} with repeats {}'.format(command, repeats))
    with tv.SamsungTv() as samsung_tv:
        if command in tv_functions_repeats:
            tv_functions_repeats[command](samsung_tv, repeats)
            return 'ok'
        else:
            return make_response(jsonify({'error': 'no mapping exists'}), 404)

@app.route('/youtube/playlist', methods=['GET'])
@auth.login_required
def get_youtube_playlists():
    print('received youtube playlist request')
    youtubeClient = youtube.YoutubeClient()
    playlists = youtubeClient.getPlaylist()
    return make_response(jsonify(playlists), 200)

@app.route('/chromecast/play/playlist/<string:name>', methods=['POST'])
@auth.login_required
def chromecast_play_first_in_playlist(name):
    print('received play first video in youtube playlist request')
    youtubeClient = youtube.YoutubeClient()
    playlistState = youtubeClient.getPlaylistStateForFirstVideoInPlaylist(name)
    if playlistState == None:
        return make_response(jsonify({'error': 'could not find playlist'}), 400)
    else:
        playlistState.save()
        chromecast.play_video(playlistState.url)
        return make_response(jsonify({'action': 'playing' }), 200)

@app.route('/chromecast/stop', methods=['POST'])
@auth.login_required
def chromecast_stop():
    print('received stop chromecast')
    chromecast.stop()
    return make_response(jsonify({'action': 'stopped' }), 200)

@app.route('/chromecast/pause', methods=['POST'])
@auth.login_required
def chromecast_pause():
    print('received pause chromecast')
    chromecast.pause()
    return make_response(jsonify({'action': 'paused' }), 200)

@app.route('/chromecast/play', methods=['POST'])
@auth.login_required
def chromecast_play():
    print('received play chromecast')
    chromecast.play()
    return make_response(jsonify({'action': 'playing' }), 200)

@app.route('/chromecast/resume', methods=['POST'])
@auth.login_required
def chromecast_resume():
    print('received resume chromecast')
    success = chromecast.resume()
    if success:
        return make_response(jsonify({'action': 'resumed' }), 200)
    else:
        return make_response(jsonify({'message': 'no previous playlist was found' }), 400)

@app.route('/chromecast/play/next', methods=['POST'])
@auth.login_required
def chromecast_play_next():
    print('received play next chromecast')
    success = chromecast.play_next()
    if success:
        return make_response(jsonify({'action': 'playing next' }), 200)
    else:
        return make_response(jsonify({'message': 'no media is playing' }), 400)

@app.route('/chromecast/play/previous', methods=['POST'])
@auth.login_required
def chromecast_play_previous():
    print('received play previous chromecast')
    success = chromecast.play_previous()
    if success:
        return make_response(jsonify({'action': 'playing previous' }), 200)
    else:
        return make_response(jsonify({'message': 'no media is playing' }), 400)

@app.route('/chromecast/playlist/info', methods=['GET'])
@auth.login_required
def chromecast_info():
    print('received get playlist info chromecast')
    info = chromecast.playlist_info()
    return make_response(jsonify({'info': info }), 200)

@app.route('/chromecast/status', methods=['GET'])
@auth.login_required
def chromecast_status():
    print('received media status chromecast')
    status = chromecast.media_status()
    return make_response(str(status), 200)

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
