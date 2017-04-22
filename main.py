from gevent import monkey;
monkey.patch_all()

import gevent
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from twython import TwythonStreamer
from config import CONF
from twitterstreamer import TwitterStreamer, TwitterWatchDog

# server side 
# Initialize and configure Flask
app = Flask(__name__)  
app.config['SECRET_KEY'] = 'secret'  
app.debug = True
# initialize SocketIo
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

@app.route('/tweets')
def tweets():
    tweets = []
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(['clinton', 'bitch']) # all the terms to search for
        tso.set_language('en') 
        tso.set_count(5)
        tso.set_include_entities(False)
        

        ts = TwitterSearch(
            consumer_key = 'JPIQgfrt5gTI90PgC2DNoLf44',
            consumer_secret = 'wt1ciclku2cftRrv1WrNY3sidoSbRQ3xSP74fKO1dafT1pVHzn',
            access_token = '15718225-77FWg39DfjuZIMRv4aqfuiEd3tM9TbmBHIFenF2tQ',
            access_token_secret = 'qx9uoD5yzsUWeBgzVqIzChO7rruAvNjhomKmqua9nsfpl'
            )

        # main part
        for tweet in ts.search_tweets_iterable(tso):
         tweets.append({'text': tweet['text'],
                         'date': tweet['created_at'],
                         'name': tweet['user']['name'],
                         'screen_name': tweet['user']['screen_name'],
                         'prof': tweet['user']['profile_image_url_https'],
                         'user_url': tweet['user']['url']})
    
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
         print(e)

    return render_template("index.html", tweets = tweets)
   
if __name__ == "__main__": #only start web server if this file is called directly  
    try:
        port = int(os.environ.get('PORT', 5000)) 
        socketio.run(app, host='0.0.0.0', port = port)
    except KeyboardInterrupt:
        pass