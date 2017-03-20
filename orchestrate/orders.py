"""
Call orders lambda service
"""
import boto3
import json

def order(event, context):
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
    response = boto3.client('lambda').invoke(
        FunctionName='orders',
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps(payload))

    return json.loads(response["Payload"].read())
