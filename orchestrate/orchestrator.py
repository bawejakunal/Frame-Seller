"""
Lamdba Orchestrator
"""

from __future__ import print_function
from order import accept, validate, orderqueue
from error import error

def handler(event, context):
    """
    delegate work
    """
    try:
        print(event)
        if event['operation'] == 'purchase':
            order_data = event['body-json']
            if validate(order_data) is False:
                return error(400, "Malformed data")

            # add to sqs and intermediate database
            response = accept(event, order_data)
            return response #map this to 202 accepted response

        elif event['operation'] == 'orderqueue':
            response = orderqueue(event)

            if response['type'] == 'result':
                return response['result']

            elif response['type'] == 'error':
                status = response['error']['http_status']
                message = response['error']['message']
                return error(status, message)
        else:
            return error(500, "Unknown operation")

    except KeyError as err:
        print(err)
        return error(400, "No resource specified")
