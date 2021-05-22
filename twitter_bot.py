import tweepy
import time
from textblob import TextBlob
import random

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

##for follower in tweepy.Cursor(api.followers).items():
##    follower.follow()
##    print (follower.screen_name)
     
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):  # this func modifies the last_seen_id file
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def tweet_sentiment(tweet):
    
    analysis = TextBlob(tweet)

    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def reply_to_tweets():
    
    print('retrieving and replying to tweets...', flush=True)
    
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')                        
                     
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        sentiment = tweet_sentiment(mention.full_text.lower())

        reply_neutral = ['Is that so', 'Maybe', 'Probably', 'Sure', 'Affirmative', 'thanks man']
        reply_angry = ["I am angry!!", "don't talk like that", "I'm gonaa report u!!"]
        
        if sentiment is 'positive':
            api.update_status(random.choice(reply_neutral) + ',  @' + mention.user.screen_name, mention.id)
        elif sentiment is 'neutral':
            api.update_status(random.choice(reply_neutral) + ',  @' + mention.user.screen_name, mention.id)
        else:
            api.update_status(random.choice(reply_angry) + ',  @' + mention.user.screen_name, mention.id)
                    
while True:
    reply_to_tweets()
    time.sleep(15)

