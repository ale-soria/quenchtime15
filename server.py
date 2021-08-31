#-*- coding: utf-8 -*-
from sanic import Sanic
from sanic_jwt_extended import JWT
from sanic_cors import CORS
from datetime import timedelta

from controllers import api


app = Sanic("qt15")
CORS(app, automatic_options=True)

app.config.RESPONSE_TIMEOUT = 45
app.config.REQUEST_TIMEOUT = 45

with JWT.initialize(app) as manager:
    manager.config.use_acl = True
    manager.config.acl_claim = "role"
    manager.config.access_token_expires = timedelta(hours=10)
    manager.config.refresh_token_expires = timedelta(minutes=30)
    manager.config.csrf_protect = True
    manager.config.csrf_request_methods = (
        'POST', 'PUT', 'PATCH', 'DELETE', 'GET')
    manager.config.jwt_csrf_header = 'X-CSRF-Token'
    manager.config.refresh_jwt_csrf_header = 'X-CSRF-Refresh'
    manager.config.secret_key = "AF3A7D8FAC625C9EC90A5D15C265BF7FC793B8E06D0B67A7D675430175B81D57EON[MlO17rwTNTOP"
    manager.config.jwt_header_key = "Authorization"
    manager.config.refresh_jwt_header_key = "X-Refresh"

app.blueprint(api)

app.run(debug=False, host="0.0.0.0", port=8000, auto_reload=True)
