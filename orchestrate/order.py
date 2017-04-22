"""
Call orders lambda service
"""
from datetime import datetime
import json
import boto3
from calendar import timegm

class Queue:
    URL = 'https://sqs.us-east-1.amazonaws.com/908762746590/Order-Queue'

def validate(order):
    """
    validate order json
    """
    _order_fields = ('product', 'stripe_token')
    _product_fields = ('url', 'price', 'id', 'links',
        'description')

    if not isinstance(order, dict):
        return False

    for field in _order_fields:
        if field not in order:
            return False
        if field == _order_fields[0] and not isinstance(order[field], dict):
            return False
        if field == _order_fields[1] and not isinstance(order[field], unicode):
            return False

    product = order['product']
    for field in _product_fields:
        if field not in product:
            print order[field], type(order[field])
            return False
        if ((field == _product_fields[0] or field == _product_fields[4]) and
                not isinstance(product[field], unicode)):
            return False
        if ((field == _product_fields[1] or field == _product_fields[2]) and
                not isinstance(product[field], int)):
            return False
        if (field == _product_fields[3] and
                not isinstance(product[field], list)):
            return False

    return True

def accept(event, order):
    """
    accept valid order json
    add to SQS and intermediate queue database
    """
    client = boto3.client('sqs')

    #create message to send
    _order_json = dict()
    _order_json['type'] = 'create_order'
    _order_json['data'] = order.copy()
    _order_json['event'] = {
        'principal-id': event['context']['authorizer-principal-id'],
        'proto': event['params']['header']['CloudFront-Forwarded-Proto'],
        'stage': event['context']['stage'],
        'host': event['params']['header']['Host']
    }

    message = json.dumps(_order_json)

    #add to sqs
    client.send_message(QueueUrl=Queue.URL, MessageBody=message)

    #add to order lambda
    payload = {
        'operation': 'orderqueue',
        'body-json': _order_json,
    }
    response = invoke_order_lambda(payload)
    return response


def invoke_order_lambda(payload, invoke='RequestResponse'):
    """
    invoke order lambda
    """
    response = boto3.client('lambda').invoke(
        FunctionName='orderqueuelambda',
        InvocationType=invoke,
        LogType='None',
        Payload=json.dumps(payload))

    return response

# def order(event):
#     """
#     extract info from event and pass on to order microservice
#     """
#     payload = {
#         'uid': event['requestContext']['authorizer']['principalId'],
#         'host': event['headers']['Host'],
#         'stage': event['requestContext']['stage'],
#         'path': event['path'],
#         'httpMethod': event['requestContext']['httpMethod'],
#         'pathParameters': event['pathParameters'],
#         'body': event['body']
#     }

#     response = invoke_order_lambda(payload, 'RequestResponse')
#     return response


# def create_order(event, status):
#     """
#     create new order
#     """

#     #convert unicode to dict
#     event['body'] = json.loads(event['body'])

#     #add order metadata
#     event['body']['orderdate'] = timegm(datetime.now().timetuple())
#     event['body']['paymentstatus'] = status

#     #call order microservice with POST request
#     response = order(event)
#     data = json.loads(response['Payload'].read())

#     return data
