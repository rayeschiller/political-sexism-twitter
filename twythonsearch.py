from twython import TwythonStreamer, Twython
from config import CONF

twitter = Twython(CONF['APP_KEY'], CONF['APP_SECRET'], CONF['OAUTH_TOKEN'], CONF['OAUTH_TOKEN_SECRET'])

results = twitter.cursor(twitter.search, q='hillary clinton bitch', lang='en', count=2)
for result in results:
    print result['text']
    print result['created_at']