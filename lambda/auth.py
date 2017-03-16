"""
Authorization Lambda function
"""

from __future__ import print_function

import json
from signup import create_customer

HTTP_ERROR = {
        400: 'Bad Request',
        403: 'Forbidden',
        401: 'Unauthorized',
        500: 'Internal Server Error'
}


def error(http_status=500, message=None):
    """
    return http error codes as suggested in best practises

    https://aws.amazon.com/blogs/compute/error-handling-patterns-in-amazon-api-gateway-and-aws-lambda/
    """  

    """
    If developer is making foolish mistake
    make them pay for it
    """
    if http_status not in HTTP_ERROR:
        http_status = 500

    err = {
        'http_status': http_status,
        'error_type': HTTP_ERROR[http_status],
        'message': message
    }
    raise Exception(json.dumps(err))

def auth_handler(event, context):
    print(event)
    if 'operation' not in event:
        return error(400, 'No operation specified')

    operation = event['operation']
    if operation == 'signup':
        return create_customer(event)
    else:
        return error(400, 'Invalid operation')
