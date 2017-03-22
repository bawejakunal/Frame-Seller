"""
Lamdba Orchestrator
"""

from __future__ import print_function
import json
import orders
import purchase
from respond import respond, error

def handler(event, context):
    """
    delegate work
    """
    print(event)
    try:
        if event['resource'].startswith('/orders'):
            try:
                response = orders.order(event)
                data = json.loads(response["Payload"].read())
                body = json.loads(data['body'])
                return respond(data['statusCode'], body)
            except (KeyError, Exception) as err:
                #in case of unhandled exception
                print(err)
                return error(500, 'Error processing order request')

        elif event['resource'].startswith('/purchase'):
            status = None
            data = purchase.buy_product(event)
            body = json.loads(data['body'])

            #return accepted with order url once
            #payment/order accepted for processing
            if int(data['statusCode']) == 202:
                status = 202
            else:
                status = data['statusCode']
            return respond(status, body)

        elif event['resource'] == '/update/order':
            print(event)
            orders.update_order(event)

        else:
            return error(500, "Unknown operation")

    except KeyError as err:
        print(err)
        return error(400, "No resource specified")