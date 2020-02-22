from flask_httpauth import HTTPTokenAuth
from app.utils import jwt_utils
from flask import request, session

auth = HTTPTokenAuth(scheme='JWT')


@auth.verify_token
def verify_token(token):
    token = request.headers.get('token') or request.values.get('token')
    if token is None:
        return False
    userid = jwt_utils.verify_token(token)
    session['userid'] = userid
    if userid:
        return True
    return False
