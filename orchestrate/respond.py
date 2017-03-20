"""
error processing module
"""

import json

def respond(code=500, result=None):
    return {
        'statusCode': str(code),
        'body': json.dumps(result),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

def error(code=500, message=None):
    body = {
        'message': message
    }
    return respond(code, body)
