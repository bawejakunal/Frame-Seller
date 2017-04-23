"""
Call orders lambda service
"""
import json
import boto3
from notify import publish, Topic
from botocore.exceptions import ClientError
from error import error

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

    #create message to publish
    _order_json = dict()
    _order_json['type'] = 'create_order'
    _order_json['data'] = order.copy()
    _order_json['event'] = {
        'principal-id': event['context']['authorizer-principal-id'],
        'proto': event['params']['header']['CloudFront-Forwarded-Proto'],
        'stage': event['context']['stage'],
        'host': event['params']['header']['Host']
    }

    #add to order lambda
    payload = {
        'operation': 'orderqueue',
        'body-json': _order_json,
    }
    response = invoke_order_lambda(payload)
    data = json.loads(response['Payload'].read())

    #publish to SNS Topic for new order
    _order_json['queue-id'] = data['oid']
    try:
        response = publish(_order_json, Topic.ORDER)
    except ClientError as err:
        print(err)
        return error(500, "Error accepting order")
    else:
        return data

def invoke_order_lambda(payload, invoke='RequestResponse'):
    """
    invoke order lambda
    """
    response = boto3.client('lambda').invoke(
        FunctionName='OrderQueueLambda',
        InvocationType=invoke,
        LogType='None',
        Payload=json.dumps(payload))

    return response
