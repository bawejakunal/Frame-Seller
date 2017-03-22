import json

def respond(resp, resp_code):
    return {
        'statusCode': resp_code,
        'body': json.dumps(resp),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

class Response:
    OK = '200'
    BAD = '400'
    FORBIDDEN = '403'
    NOT_FOUND = '404'
    INT_SER_ERR = '500'
