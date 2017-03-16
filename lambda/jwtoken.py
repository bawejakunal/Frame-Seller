"""
module to generate jwt token
"""

import os
from calendar import timegm
import datetime
from error import error
from lib import jwt
from lib.jwt.exceptions import MissingRequiredClaimError
from lib.jwt import InvalidTokenError, DecodeError

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

def verify_jwt(body)