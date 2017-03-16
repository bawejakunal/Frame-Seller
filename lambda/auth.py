"""
Authorization Lambda function
"""

from __future__ import print_function

import json
from signup import create_customer
from error import error

def auth_handler(event, context):
    print(event)
    if 'operation' not in event:
        return error(400, 'No operation specified')

    operation = event['operation']
    if operation == 'signup':
        return create_customer(event)
    else:
        return error(400, 'Invalid operation')
