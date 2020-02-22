import jwt
import datetime
from public import config

key = config.SECRET_KEY


def create_token(userid):
    payload = {
        "iat": datetime.datetime.now(),
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
        "id": str(userid),
    }
    token = jwt.encode(payload, key, algorithm='HS256').decode('utf-8')
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
    except(jwt.exceptions.ExpiredSignatureError,
           jwt.exceptions.InvalidSignatureError,
           jwt.exceptions.DecodeError) as e:
        return print(e)
    if payload:
        return payload['id']
    return None
