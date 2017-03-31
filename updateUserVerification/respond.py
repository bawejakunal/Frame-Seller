"""
error processing module
"""
import json

def respond(code=500, result=None, headers=None):
    response = {
        'statusCode': str(code),
        'body': json.dumps(result),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

    if headers is not None and type(headers) is dict:
        response['headers'].update(headers)

    return response

def error(code=500, message=None):
    body = {
        'message': message
    }
    return respond(code, body)
