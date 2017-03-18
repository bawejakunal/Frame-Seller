"""
Authorization Lambda function
"""

from __future__ import print_function

from signup import create_customer
from login import login_customer
from error import error
from policy import policy_builder

def auth_handler(event, context):

    #check if request is for authorization
    if 'authorizationToken' in event:
        return policy_builder(event, context)

    #signup or login operation
    if 'operation' not in event:
        return error(500, 'No operation specified')

    if 'body-json' not in event:
        return error(400, 'Malformed request')

    operation = event['operation']
    body = event['body-json']

    if operation == 'signup':
        return create_customer(body)
    elif operation == 'login':
        return login_customer(body)
    else:
        return error(400, 'Invalid operation')
