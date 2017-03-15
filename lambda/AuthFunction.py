from __future__ import print_function

import boto3
import json

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))
    #operation = event['httpMethod']
    #print(operation)
    if "type" not in event:
        return respond(ValueError('Bad Request, no operation specified'))
    
    type = event['type']
    
    if type == 'signup':
        # Execute Sign Up routine
        signup(event)
        pass
    elif type == 'login':
        # Execute Login routine
        pass
    elif type == 'verifytoken':
        # Execute Verify Token routine
        pass
    else:
        return respond(ValueError('Bad Request, illegal operation specified'))
    
    return "Hello"
    
    """operations = {
        'POST': lambda dynamo, x: dynamo.put_item(**x)
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        dynamo = boto3.resource('dynamodb').Table("User")
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))"""
