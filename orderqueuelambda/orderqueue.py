"""
Order queue handling lambda
"""

from __future__ import print_function
from orderdb import add_order, order_queue
from queue import update_orders
from error import error

def handler(event, context):
    #signup or login operation
    try:
        print(event)
        if 'operation' not in event or 'body-json' not in event:
            return error(400, 'Invalid operation')

        operation = event['operation']

        # update order queued status to created
        if operation == 'order-create':
            update_orders(event)

        # add new orders to queue
        elif operation == 'purchase':
            order = add_order(event)
            return order

        # get status of queued orders
        elif operation == 'orderqueue':
            result = order_queue(event)
            
            if result is None:
                return error(404, "No order found")
            elif isinstance(result, dict) and'redirect_url' in result:
                return error(301, result['redirect_url'])

            return result

        else:
            return error(400, 'Invalid operation')

    except KeyError as err:
        print(err)
        return error(400, 'Invalid operation')
