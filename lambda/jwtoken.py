"""
module to generate jwt token
"""

import os
from calendar import timegm
import datetime
from error import error
from lib import jwt
from lib.jwt import (ExpiredSignatureError, InvalidTokenError,
                     MissingRequiredClaimError)

try:
    ALGORITHM = os.environ['JWT_ALGORITHM']
    TIME_DELTA = int(os.environ['JWT_TIME_DELTA'])
    SECRET = os.environ['JWT_SECRET']
except KeyError:
    error(500, 'Error loading JWT environment')

def create_jwt(payload):
    """
    generate jwt token
    """
    exp = datetime.datetime.now() + datetime.timedelta(seconds=TIME_DELTA)
    exp = timegm(exp.timetuple()) #Unix timestamp is always int

    payload['exp'] = exp
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {'token':token}

def verify_jwt(token):
    """
    verify jwt
    """

    options = {
        'verify_signature': True,
        'verify_exp': True,
        'require_exp': True
    }

    try:
        payload = jwt.decode(token, SECRET, options=options)
        return payload
    except (ExpiredSignatureError, InvalidTokenError, \
            MissingRequiredClaimError):
        return None
