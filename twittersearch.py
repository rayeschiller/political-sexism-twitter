'''
Twitter search API using twittersearch wrapper 
'''

# enable debugging
import cgitb
from TwitterSearch import *

def getTweets():
    wordlist = []
    # sexistWords = ['whore', 'pussy','cunt','skank','bitch', 'slut', 'bimbo', 'shrill', 'witch', 'Feminazi', 'dyke', 'lesbian', 'kitchen']
    politicians = ['HillaryClinton','Hillary Clinton', 'Elizabeth Warren', 'SenWarren', 'ElizabethWarren', 'Ivanka', 'IvankaTrump', 'Kellyanne Conway', 'KellyannePolls', 'NancyPelosi', 'Nancy Pelosi']
    sexistWords = ['bitch']
    for word in sexistWords:
        for politician in politicians:
            wordlist.append(word + ' ' + politician)
    # print(wordlist)
    tweets = []
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        '''TODO: Figure out how to search list of keywords as OR possibilities'''

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
            print(tweet['text'])
        #  tweets.append({'text': tweet['text'],
        #                  'date': tweet['created_at'],
        #                  'name': tweet['user']['name'],
        #                  'screen_name': tweet['user']['screen_name'],
        #                  'prof': tweet['user']['profile_image_url_https'],
        #                  'user_url': tweet['user']['url']})
    
        # print(tweets)
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
         print(e)

if __name__ == "__main__":
    getTweets()