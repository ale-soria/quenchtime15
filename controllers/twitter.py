from sanic import Blueprint
from sanic.request import Request

twitter = Blueprint('twitter', 'tw')

@twitter.route('/')
async def gettweets(request: Request):
    pass