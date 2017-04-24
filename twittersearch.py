# enable debugging
import cgitb
from TwitterSearch import *

def getTweets():
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