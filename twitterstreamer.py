from twython import TwythonStreamer, Twython
from config import CONF
import gevent
import sqlite3 as sql

# Twitter stream class 
class TwitterStreamer(TwythonStreamer):
    # initialize twitter stream and tweet queue
    def __init__(self, *args, **kwargs):
        TwythonStreamer.__init__(self, *args, **kwargs)
        print("Initialized TwitterStreamer.")
        self.queue = gevent.queue.Queue()
        


    # On successful stream connection put tweet in queue
    def on_success(self,data):
        # filter tweets to not be responses, medium filter level, and in english 
        # print(data)
        if data['in_reply_to_status_id'] == None and data['in_reply_to_screen_name'] == None and data['lang'] == 'en':

            if data.has_key('extended_tweet'):
                tweettext = data['extended_tweet']['full_text']
                print('extended tweet')
            elif data.has_key('retweeted_status'):
                try:
                    tweettext = data['retweeted_status']['extended_tweet']['full_text']
                except:
                    tweettext = data['retweeted_status']['text']
                print('retweeted_status')
            else:
                tweettext = data['text']
                print('regular tweet')
            location = ''
            if data['place'] != None:
                location = data['place']['full_name']
            elif data.has_key('quoted_status'):
                try:
                    location = data['quoted_status']['place']['full_name']
                except: 
                    pass
            elif data.has_key('retweeted_status'):
                try:
                    location = data['retweeted_status']['place']['full_name']
                except:
                    pass
            
            conn = sql.connect('database.db')
            cur = conn.cursor()
            # cur.execute("DROP TABLE tweets")
            # cur.execute("CREATE TABLE IF NOT EXISTS tweets(tweet text, created_at text) ")
            # cur.execute("ALTER TABLE tweets ADD location text")
            cur.execute("INSERT INTO tweets(tweet, created_at, username, location) VALUES (?,?,?,?)", (tweettext, data['created_at'], data['user']['screen_name'], location))
            conn.commit()
            conn.close()
            # print('table action executed')
            # print('text is ' + tweettext)
            self.queue.put_nowait(data)
            if self.queue.qsize() > 10000:
                self.queue.get()          
   
    # On error 
    def on_error(self, status_code, data): 
        print status_code, "TwitterStreamer stopped because of an error"
        self.disconnect()   

# Twitter Watch Dog class
class TwitterWatchDog:
    def __init__(self):
        #create word list for combining sexist words with female politicians
        wordlist = []
        for word in CONF['SEXISTWORDS']:
            for politician in CONF['POLITICIANS']:
                wordlist.append(word + ' ' + politician)
        # print(wordlist)
        self.streamer = TwitterStreamer(CONF['APP_KEY'], CONF['APP_SECRET'], CONF['OAUTH_TOKEN'], CONF['OAUTH_TOKEN_SECRET'])
        self.green = gevent.spawn(self.streamer.statuses.filter, track=wordlist)

    def check_alive(self):
        if self.green.dead:
            # stop everything
            print('checking if alive')
            self.streamer.disconnect()
            self.green.kill()
            # restart 
            self.__init__()