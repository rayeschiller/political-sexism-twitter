# -*- coding: utf8 -*-
from gevent import monkey;
monkey.patch_all()

from flask_bootstrap import Bootstrap
import gevent
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from TwitterSearch import *
from config import CONF
from twitterstreamer import TwitterStreamer, TwitterWatchDog
import sqlite3 as sql
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

@app.route('/map')
def map():
    return render_template("map.html")

 # in terminal handling
@socketio.on('connect', namespace = '/tweets')
def tweets_connect():
    print(' connected on server side')
    tweets = getTweets()
    for tweet in tweets:
        emit('tweet', tweet, broadcast=True)
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

@app.route('/about')
def about():
    return render_template("about.html")

#Route for tweet page for dems vs reps
@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT DISTINCT * FROM tweets WHERE tweet LIKE '%Hillary%' OR tweet LIKE '%Warren%' OR tweet LIKE '%Pelosi%' ORDER BY created_at DESC")
   democrats = cur.fetchall()
   cur.execute("SELECT DISTINCT * FROM tweets WHERE tweet LIKE '%Kellyanne%' OR tweet LIKE '%Ivanka%' OR tweet LIKE '%Melania%'")
   republicans = cur.fetchall()


   return render_template("list.html", democrats=democrats, republicans=republicans)

#Using Twitter Search to get most recent sexist tweets to populate feed when first go onto the page
def getTweets():
    wordlist = []
    politicians = CONF['POLITICIANS']
    sexistWords = ['bitch']
    for word in sexistWords:
       for politician in politicians:
           wordlist.append(word + ' ' + politician)
    tweets = []
    try: 
        tso = TwitterSearchOrder()
        tso.set_keywords(wordlist, or_operator = True) # all the terms to search for
        tso.set_language('en')

        ts = TwitterSearch(consumer_key = CONF['APP_KEY'],consumer_secret = CONF['APP_SECRET'],access_token = CONF['OAUTH_TOKEN'],access_token_secret = CONF['OAUTH_TOKEN_SECRET'])
        for tweet in ts.search_tweets_iterable(tso):
            tweets.append(tweet)
        return tweets
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
         print(e)


if __name__ == "__main__": #only start web server if this file is called directly  
    try:
        port = int(os.environ.get('PORT', 5000)) 
        socketio.run(app, host='0.0.0.0', port = port)
    except KeyboardInterrupt:
        pass