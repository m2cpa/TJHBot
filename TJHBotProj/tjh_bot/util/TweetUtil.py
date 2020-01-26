'''
Created on 2020/01/22

@author: m2(@m2cpa)
'''
import os
import tweepy

API_KEY = os.environ["CONSUMER_KEY"]
API_SECRET_KEY = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN_KEY"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

api = None

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


################################################
# ツイートする
################################################
def tweet(tweet_messages, exist_message, not_exist_message=""):
    if tweet_messages:
        api.update_status(exist_message)
        for tweet_message in tweet_messages:
            api.update_status(tweet_message)

    else:
        if not_exist_message:
            api.update_status(not_exist_message)
