"""
Order queue handling lambda
"""

from __future__ import print_function
from orderdb import add_order, construct_url
from error import error

def handler(event, context):
    #signup or login operation
    try:
        print(event)
        if 'operation' not in event or 'body-json' not in event:
            return error(400, 'Invalid operation')

        operation = event['operation']
        body = event['body-json']

        # update order queued status to created
        if operation == 'update':
            pass

        # add new orders to queue
        elif operation == 'orderqueue':
            order_id = add_order(body)
            url = construct_url(body['event'], order_id)
            return {
                'order-id': order_id,
                'Location': url
            }

        # get status of queued orders
        elif operation == 'getorderstatus':
            pass

        else:
            return error(400, 'Invalid operation')

    except KeyError as err:
        print(err)
        return error(400, 'Invalid operation')
