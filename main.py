from flask import Flask, render_template
import cgitb
import requests
from TwitterSearch import *

cgitb.enable()

app = Flask(__name__)

# routing/mapping a url on website to a python function 
@app.route('/') #root directory, home page of website, called a decorator
def index():
    tweets = []

    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(['hello']) # all the terms to search for
        tso.set_language('en') 
        tso.set_include_entities(False)

        ts = TwitterSearch(
            consumer_key = 'JPIQgfrt5gTI90PgC2DNoLf44',
            consumer_secret = 'wt1ciclku2cftRrv1WrNY3sidoSbRQ3xSP74fKO1dafT1pVHzn',
            access_token = '15718225-77FWg39DfjuZIMRv4aqfuiEd3tM9TbmBHIFenF2tQ',
            access_token_secret = 'qx9uoD5yzsUWeBgzVqIzChO7rruAvNjhomKmqua9nsfpl'
            )

        # main part
        for tweet in ts.search_tweets_iterable(tso):
           # tweets.append('@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ))
           tweets.append(tweet['text'])
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

    return render_template("index.html", tweets = tweets)

@app.route('/tweets')
def tweets():
    return "<h2>Tuna is good</h2>"



if __name__ == "__main__": #only start web server if this file is called directly  
    port = int(os.environ.get('PORT', 33507)) 
    app.run(debug=True) #starts app on web server 
