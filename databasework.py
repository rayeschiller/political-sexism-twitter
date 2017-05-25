'''
Database Work
'''
import sqlite3 as sql
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
 
conn = sql.connect('database.db')
cur = conn.cursor()
# cur.execute("INSERT INTO tweets(tweet, created_at, username, location) VALUES (?,?,?,?)", (tweettext, data['created_at'], data['user']['screen_name'], location))
cur.execute("SELECT * FROM tweets WHERE tweet LIKE '%Hillary%'")
words = cur.fetchall()
conn.commit()
conn.close()

words = list(words)
# words = ''.join(words)

words = word_tokenize(words[0])
# words = ([word for word in words if word not in stop_words])

print(words)
