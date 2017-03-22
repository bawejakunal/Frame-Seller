"""
Call orders lambda service
"""
from datetime import datetime
import json
import boto3
from calendar import timegm

def invoke_order_lambda(payload, invoke='RequestResponse'):
    """
    invoke order lambda
    """
    response = boto3.client('lambda').invoke(
        FunctionName='orders',
        InvocationType=invoke,
        LogType='None',
        Payload=json.dumps(payload))

    return response

def order(event):
    """
    extract info from event and pass on to order microservice
    """
    payload = {
        'uid': event['requestContext']['authorizer']['principalId'],
        'host': event['headers']['Host'],
        'stage': event['requestContext']['stage'],
        'path': event['path'],
        'httpMethod': event['requestContext']['httpMethod'],
        'pathParameters': event['pathParameters'],
        'body': event['body']
    }

    response = invoke_order_lambda(payload, 'RequestResponse')
    return response


def create_order(event, status):
    """
    create new order
    """

    #convert unicode to dict
    event['body'] = json.loads(event['body'])

    #add order metadata
    event['body']['orderdate'] = timegm(datetime.now().timetuple())
    event['body']['paymentstatus'] = status

    #call order microservice with POST request
    response = order(event)
    data = json.loads(response['Payload'].read())

    return data

def update_order(payload):
    """
    update order payload async
    """
    invoke_order_lambda(payload, 'Event')
