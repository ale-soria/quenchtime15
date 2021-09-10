import os
import tweepy
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from json import dumps

twitter = Blueprint('twitter')


TWEEPY_CONSUMER_KEY = 'zPD17xsnd34YG3PDgUTgrv0qK'
TWEEPY_CONSUMER_SECRET = 'fGCxbP1mjUkG2c5QTmWif5dCXQ3syOPMTSoWPFKdeGAU5kQjR9'
ACCESS_TOKEN = '68504097-hc2TJqFrEqdzeVFh83IqVMWVGEMQYXQyuWDGDGWOH'
ACCESS_SECRET = 'fLwSPNkvqJx0pUk0cvlWv5aftOLNzfpwE5nckIYVf1Pix'

auth = tweepy.OAuthHandler(
    TWEEPY_CONSUMER_KEY, TWEEPY_CONSUMER_SECRET)
auth.set_access_token(
    ACCESS_TOKEN, ACCESS_SECRET)


def twitterAuth():
    try:
        api = tweepy.API(auth)
        return api
    except tweepy.TweepError as e:
        print(e)


def get_public_tweets(params):
    try:
        api = twitterAuth()
        if not 'geoloc' in params or not 'limit' in params or not 'keywords' in params:
            return 'Missing parameters'
        pages = tweepy.Cursor(
            api.search, 
            q=params['keywords'],
            geocode='{},{},{}'.format(params['geoloc'][0], params['geoloc'][1], params['geoloc'][2]),
            lang='en', 
            count=params['n_per_page'],
            result_type='mixed').items(params['limit'])
        r = []
        for page in pages:
            # page._json = dumps(page._json)
            # print(page._json['id'])
            r.append({
                'id': page._json['id'],
                'text': page._json['text'],
                'users_in_mentions': page._json['entities'],
                'user_fullname': page._json['user']['name'],
                'user_username': page._json['user']['screen_name'],
                'user_location': page._json['user']['location'],
                'place': page._json['place']['name'],
                'place_type': page._json['place']['place_type'],
                'place_fullname': page._json['place']['full_name'],
                'place_country_code': page._json['place']['country_code'],      
            })
        return r
    except tweepy.TweepError as e:
        print(e)


@twitter.route('/tweets')
async def gettweets(request: Request):
    res = get_public_tweets(request.json)
    return json(res)
