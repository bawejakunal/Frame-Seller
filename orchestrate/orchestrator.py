"""
Lamdba Orchestrator
"""

from __future__ import print_function
import json
import boto3
import orders
from respond import respond, error

def handler(event, context):
    """
    delegate work
    """
    print(event)
    if event['resource'].startswith('/orders'):
        try:
            response = orders.order(event, context)
            data = json.loads(response["Payload"].read())
            body = json.loads(data['body'])
            return respond(data['statusCode'], body)
        except Exception as err:
            #in case of unhandled exception
            print(err)
            return error(500, 'Error processing order request')

    elif event['resource'].startswith('/purchase'):
        return respond(202, 'Order accpeted for processing')
    # elif event['resource'].startswith('/purchase'):
    #     data = purchase.buy_product(event, context)
    #     if int(data['statusCode']) == 200:
    #         return respond(202, 'Order Accepted')
    #     else:
    #         return respond(data['statusCode'], data['body'])

    else:
        raise Exception('Unspecified Operation')
