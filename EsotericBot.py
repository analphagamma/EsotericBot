import tweepy
import TweetCreator
import json
from random import randint
from datetime import date
import os
import horoscopecrawler

class TwitterAPI:
    def __init__(self):
        #Authentication data. DO NOT CHANGE!
        with open('auth_codes.json', 'r+') as f: auth_codes = json.load(f)
        
        CONSUMER_KEY = auth_codes['CONSUMER_KEY']
        CONSUMER_SECRET = auth_codes['CONSUMER_SECRET']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        ACCESS_TOKEN = auth_codes['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = auth_codes['ACCESS_TOKEN_SECRET']
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        '''Makes a text tweet'''
        self.api.update_status(status=message)
 
zodiac = [
        'aries',
        'taurus',
        'gemini',
        'cancer',
        'leo',
        'virgo',
        'libra',
        'scorpio',
        'sagittarius',
        'capricorn',
        'aquarius',
        'pisces'
]


#######################################


def post_horoscope():
    ''' * creates Twitterbot object
        * iterates through zodiac signs
        * checks if tweet is already made
        * creates text
        * posts tweet
        * saves tweet in txt format'''
     
    #instantiating bot
    EsotericBot = TwitterAPI()
    print("Waking up bot...")
   
    with open('tweet_log.json', 'r+') as f: tweet_log = json.load(f)
    f.close()       
     
   
    for sign in zodiac:
        
        #checking in tweet_log if tweet has already been made on current day
        try:
            if tweet_log[sign] == str(date.today()):
                print('Horoscope for ' + sign + ' has already been tweeted today.\nSkipping...\n')
                continue
            else:
                tweet_log[sign] = str(date.today())
        except KeyError:
            tweet_log[sign] = str(date.today())
            
        #creating tweet - it must be less than or equal to 140 characters
        confirmation = ''
        while  confirmation != 'y':
                        
            text_body = TweetCreator.create_tweet_text()
        
            tweet_text = '#' + sign + '\n' + text_body
            if len(tweet_text) > 260:
                confirmation = ''
            else:
                print('\n\"' + tweet_text + '\"\n')
                confirmation = 'y'
            
        #saving tweet
        fname = 'tweet_' + sign + str(date.today()) + '.txt'
        with open(os.path.join('./tweets', fname), 'a') as f: f.write(tweet_text)
        f.close()
        
        #posting tweet    
        print('Posting tweet...')
        EsotericBot.tweet(tweet_text)
        print('Done.')
               
        with open('tweet_log.json', 'w+') as f: json.dump(tweet_log, f)
        f.close()
    
    print('Done.')
        
        
#########################################

if __name__ == '__main__':
    horoscopecrawler.scrape()
    TweetCreator.initial_training()
    post_horoscope()
