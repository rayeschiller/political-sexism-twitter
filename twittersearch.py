# enable debugging
import cgitb
from TwitterSearch import *

cgitb.enable()

print("Content-Type: text/plain;charset=utf-8")
print()

print("Hello World!")


try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['bitch', 'elizabeth warren']) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'JPIQgfrt5gTI90PgC2DNoLf44',
        consumer_secret = 'wt1ciclku2cftRrv1WrNY3sidoSbRQ3xSP74fKO1dafT1pVHzn',
        access_token = '15718225-77FWg39DfjuZIMRv4aqfuiEd3tM9TbmBHIFenF2tQ',
        access_token_secret = 'qx9uoD5yzsUWeBgzVqIzChO7rruAvNjhomKmqua9nsfpl'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) + '\n')

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)