from twython import TwythonStreamer, Twython
from config import CONF
import gevent

# Twitter stream class 
class TwitterStreamer(TwythonStreamer):
    # initialize twitter stream and tweet queue
    def __init__(self, *args, **kwargs):
        TwythonStreamer.__init__(self, *args, **kwargs)
        print("Initialized TwitterStreamer.")
        self.queue = gevent.queue.Queue()

    # On successful stream connection put tweet in queue
    def on_success(self,data):
        if data['in_reply_to_status_id'] == None and data['in_reply_to_screen_name'] == None:
            self.queue.put_nowait(data)
            # print(data)
            # print('\n\n')
            # if 'extended_tweet' in data:
            #     print('full text' + data['extended_tweet']['full_text'])
            # print('small text' + data['text'])
            if self.queue.qsize() > 10000:
                self.queue.get()           

    # On error 
    def on_error(self, status_code, data): 
        print status_code, "TwitterStreamer stopped because of an error"
        self.disconnect()   

# Twitter Watch Dog class
class TwitterWatchDog:
    def __init__(self):
        wordlist = []
        sexistWords = ['whore', 'pussy','cunt','skank', 'angry','bitch', 'slut', 'bimbo', 'shrill', 'husband', 'witch', 'PMS', 'Feminazi', 'dyke', 'dragon lady', 'lesbian', 'kitchen', 'menopause']
        politicians = ['HillaryClinton','Hillary Clinton', 'Elizabeth Warren', 'SenWarren', 'ElizabethWarren', 'Ivanka', 'IvankaTrump', 'Kellyanne Conway', 'KellyannePolls', 'NancyPelosi', 'Nancy Pelosi']
        for word in sexistWords:
            for politician in politicians:
                wordlist.append(word + ' ' + politician)
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