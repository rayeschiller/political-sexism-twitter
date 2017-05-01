'''
Twitter Search API using Twython
'''
from twython import TwythonStreamer, Twython
from config import CONF

twitter = Twython(CONF['APP_KEY'], CONF['APP_SECRET'], CONF['OAUTH_TOKEN'], CONF['OAUTH_TOKEN_SECRET'])
wordlist = []
sexistWords = ['bitch']
politicians = ['Hillary Clinton', 'Elizabeth Warren']
# sexistWords = ['whore', 'pussy','cunt','skank', 'angry','bitch', 'slut', 'bimbo', 'shrill', 'husband', 'witch', 'PMS', 'Feminazi', 'dyke', 'dragon lady', 'lesbian', 'kitchen', 'menopause']
# politicians = ['HillaryClinton','Hillary Clinton', 'Elizabeth Warren', 'SenWarren', 'ElizabethWarren', 'Ivanka', 'IvankaTrump', 'Kellyanne Conway', 'KellyannePolls', 'NancyPelosi', 'Nancy Pelosi']
for word in sexistWords:
    for politician in politicians:
        wordlist.append(word + ' ' + politician)
results = twitter.cursor(twitter.search, q=wordlist, lang='en', count='4')

for result in results:
    print result
    # print result['created_at']