"""
Authorization Lambda function
"""

from __future__ import print_function

import json
from signup import create_customer
from login import login_customer
from error import error

def auth_handler(event, context):
    print(event)
    body = event['body-json']
    if 'operation' not in body:
        return error(400, 'No operation specified')

    operation = body['operation']
    if operation == 'signup':
        return create_customer(body)
    elif operation == 'login':
        return login_customer(body)
    else:
        return error(400, 'Invalid operation')
