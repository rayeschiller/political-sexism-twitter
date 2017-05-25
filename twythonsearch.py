'''
Twitter Search API using Twython
'''
from twython import TwythonStreamer, Twython
from config import CONF

twitter = Twython(CONF['APP_KEY'], CONF['APP_SECRET'], CONF['OAUTH_TOKEN'], CONF['OAUTH_TOKEN_SECRET'])
wordlist = []
sexistWords = ['bitch', 'cunt', 'pussy', 'skank', 'shrill']
politicians = ['Hillary Clinton']
# sexistWords = ['whore', 'pussy','cunt','skank', 'angry','bitch', 'slut', 'bimbo', 'shrill', 'husband', 'witch', 'PMS', 'Feminazi', 'dyke', 'dragon lady', 'lesbian', 'kitchen', 'menopause']
# politicians = ['HillaryClinton','Hillary Clinton', 'Elizabeth Warren', 'SenWarren', 'ElizabethWarren', 'Ivanka', 'IvankaTrump', 'Kellyanne Conway', 'KellyannePolls', 'NancyPelosi', 'Nancy Pelosi']
for word in sexistWords:
    for politician in politicians:
        wordlist.append(word + ' ' + politician)

results = twitter.cursor(twitter.search, q='morning coffee', lang='en')

for result in results:
    print result
    # print result['created_at']