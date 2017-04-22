from twython import TwythonStreamer
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
        self.queue.put_nowait(data)
        if self.queue.qsize() > 10000:
            self.queue.get()
        # if 'text' in data:
        #     print data['text'].encode('utf-8')             

    def on_error(self, status_code, data): 
        print status_code, "TwitterStreamer stopped because of an error"
        self.disconnect()

# Twitter Watch Dog class
class TwitterWatchDog:
    def __init__(self):
        wordlist = ['clinton']
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