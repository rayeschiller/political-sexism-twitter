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
        wordlist = ['whore hillary,pussy hillary, cunt hillary, skank hillary, bitch hillary, slut hillary, bimbo hillary, shrill hillary, feminazi hillary, hillary kitchen, fuck hillary, whore clinton,pussy clinton, cunt clinton, skank clinton, bitch clinton, slut clinton, bimbo clinton, shrill clinton, feminazi clinton, fuck clinton, clinton kitchen, whore ivanka,pussy ivanka, cunt ivanka, skank ivanka, bitch ivanka, slut ivanka, bimbo ivanka, shrill ivanka, feminazi ivanka, ivanka kitchen, fuck ivanka,whore ElizabethWarren,pussy ElizabethWarren, cunt ElizabethWarren, skank ElizabethWarren, bitch ElizabethWarren, slut ElizabethWarren, bimbo ElizabethWarren, shrill ElizabethWarren, feminazi ElizabethWarren, ElizabethWarren kitchen, fuck ElizabethWarren, whore Elizabeth Warren,pussy Elizabeth Warren, cunt Elizabeth Warren, skank Elizabeth Warren, bitch Elizabeth Warren, slut Elizabeth Warren, bimbo Elizabeth Warren, shrill Elizabeth Warren, feminazi Elizabeth Warren, Elizabeth Warren kitchen, fuck Elizabeth Warren, ']
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