# -*- coding: utf8 -*-
from gevent import monkey;
monkey.patch_all()

from flask_bootstrap import Bootstrap
import gevent
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from twython import TwythonStreamer
from config import CONF
from twitterstreamer import TwitterStreamer, TwitterWatchDog

# server side 
# Initialize and configure Flask and SocketIO
app = Flask(__name__)  
Bootstrap(app)
app.config['SECRET_KEY'] = 'secret'  
app.debug = True
socketio = SocketIO(app)

watchDog = TwitterWatchDog()
# routing/mapping a url on website to a python function 
@app.route('/') #root directory, home page of website, called a decorator
def index():
    watchDog.check_alive()
    return render_template("index.html")

 # in terminal handling
@socketio.on('connect', namespace = '/tweets')
def tweets_connect():
    print(' connected on server side')
    watchDog.check_alive()
    while True:
        try:
            tweet = watchDog.streamer.queue.get(timeout=5)
        except gevent.queue.Empty:
            watchDog.check_alive()
        else:
            emit('tweet', tweet, broadcast=True)

@socketio.on('disconnect', namespace = '/tweets')
def tweets_disconnect():
    watchDog.check_alive()
    print('server disconnected')

# @app.route('/tweets2')

   
if __name__ == "__main__": #only start web server if this file is called directly  
    try:
        port = int(os.environ.get('PORT', 5000)) 
        socketio.run(app, host='0.0.0.0', port = port)
    except KeyboardInterrupt:
        pass