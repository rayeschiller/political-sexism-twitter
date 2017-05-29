'''
Twitter search API using twittersearch wrapper for database insertion 
'''

# enable debugging
import cgitb
from TwitterSearch import *
import sqlite3 as sql
from config import CONF
def getTweets():
    wordlist = []
    # sexistWords = ['whore', 'pussy','cunt','skank','bitch', 'slut', 'bimbo', 'shrill', 'witch', 'Feminazi', 'dyke', 'lesbian', 'kitchen']
    politicians = ['HillaryClinton','Hillary Clinton', 'Elizabeth Warren', 'SenWarren', 'ElizabethWarren', 'Ivanka', 'IvankaTrump', 'Kellyanne Conway', 'KellyannePolls', 'NancyPelosi', 'Nancy Pelosi']
    sexistWords = ['whore', 'bitch']
    for word in sexistWords:
        for politician in politicians:
            wordlist.append(word + ' ' + politician)
    # print(wordlist)
    tweets = []
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object

        tso.set_keywords(wordlist, or_operator = True) # all the terms to search for
        tso.set_language('en') 
        tso.set_count(10)
        tso.set_include_entities(False)
        

        ts = TwitterSearch(
            consumer_key = 'JPIQgfrt5gTI90PgC2DNoLf44',
            consumer_secret = 'wt1ciclku2cftRrv1WrNY3sidoSbRQ3xSP74fKO1dafT1pVHzn',
            access_token = '15718225-77FWg39DfjuZIMRv4aqfuiEd3tM9TbmBHIFenF2tQ',
            access_token_secret = 'qx9uoD5yzsUWeBgzVqIzChO7rruAvNjhomKmqua9nsfpl'
            )

        # main part
        for tweet in ts.search_tweets_iterable(tso):
            if tweet.has_key('extended_tweet'):
                tweettext = tweet['extended_tweet']['full_text']
                print('extended tweet')
            elif tweet.has_key('retweeted_status'):
                try:
                    tweettext = tweet['retweeted_status']['extended_tweet']['full_text']
                except:
                    tweettext = tweet['retweeted_status']['text']
                print('retweeted_status')
            else:
                tweettext = tweet['text']
                print('regular tweet')
            location = ''
            if tweet['place'] != None:
                location = tweet['place']['full_name']
            elif tweet.has_key('quoted_status'):
                try:
                    location = tweet['quoted_status']['place']['full_name']
                except: 
                    pass
            elif tweet.has_key('retweeted_status'):
                try:
                    location = tweet['retweeted_status']['place']['full_name']
                except:
                    pass
           
            con = sql.connect('database.db')
            cur = con.cursor()   
            try:                         
                cur.execute("""INSERT INTO tweets (tweet, created_at,username,location) VALUES (?,?,?,?)""",('search: ' + tweettext, tweet['created_at'], tweet['user']['screen_name'], location))
                print('database insert')
                con.commit()
            except:
                con.rollback()
                print "error in insert operation"
            con.close()       
            print(tweet['text'])
       
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
         print(e)

if __name__ == "__main__":
    getTweets()