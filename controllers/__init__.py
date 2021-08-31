from sanic import Blueprint
from .twitter import twitter

api = Blueprint.group(twitter, url_prefix='api')
