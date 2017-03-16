"""
module to generate jwt token
"""

import time
import datetime
import jwt
from jwt.exceptions import MissingRequiredClaimError
from jwt import InvalidTokenError, DecodeError

ALGORITHM = 'HS256'
SECRET = 'SECRET'
TIME_DELTA = 3600 #seconds

def create_jwt(payload):
    """
    generate jwt token
    """
    exp = datetime.datetime.now() + datetime.timedelta(seconds=TIME_DELTA)
    exp = int(time.mktime(exp.timetuple())) #Unix timestamp is always int

    payload['exp'] = exp
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {'token':token}
