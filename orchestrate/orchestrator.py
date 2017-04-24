"""
Lamdba Orchestrator
"""

from __future__ import print_function
from order import accept, validate, orderqueue

def handler(event, context):
    """
    delegate work
    """
    try:
        print(event)
        if event['operation'] == 'purchase':
            order_data = event['body-json']
            if validate(order_data) is False:
                return error(400, "Malformed purchase order")
            # add to sqs and intermediate database
            response = accept(event)
            return response

        elif event['operation'] == 'orderqueue':
            response = orderqueue(event)
            return response
        
        else:
            return error(500, "Unknown operation")

    except KeyError as err:
        print(err)
        return error(400, "No resource specified")
