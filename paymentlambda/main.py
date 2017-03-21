"""
handle payment processing
"""
import json
from payment import create_charge
from respond import respond, error

def handler(event, context):
    """
    payment handler
    """
    if 'operation' not in event:
        return error(400, 'No operation specified')

    if event['operation'] == 'charge':
        charge = create_charge(event)
        if charge is None:
            print('Payment Failed')
            return error(500, 'Payment Failed')
        else:
            return respond(201, 'Created Payment')
    else:
        return error(400, 'Unknown operation')
