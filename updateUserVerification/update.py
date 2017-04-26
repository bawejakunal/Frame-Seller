"""
handle user verification update
"""

from __future__ import print_function
import urllib
import json
import boto3
from respond import error, respond

def handler(event, context):
    """
    user verification handler
    """
    print(event)
    if 'body' not in event:
        return error(400, 'Bad request')

    client = boto3.client('stepfunctions')
    body = json.loads(event['body'])

    """
    decoding parameters (since we are sending encoded parameters)
    """
    task_token = urllib.unquote_plus(body['taskToken'])
    _jwt_token = urllib.unquote_plus(body['vToken'])

    payload = {
        'operation': 'verify',
        'body-json':{
            'verify_token': _jwt_token
        }
    }
    """
    Send Task Success message to Step Function to let the statemachine
    proceed further
    """
    try:
        response = client.send_task_success(taskToken=task_token,
                                output=json.dumps(payload))

        #accepted for verification user should login to verify
        #alternatively we can send mail
        return respond(200, 'Verification Request Accepted')

    except Exception as err:
        print(err)
        return error(400, 'Bad request')
