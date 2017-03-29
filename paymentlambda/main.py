"""
handle payment processing
"""
import json
from payment import create_charge, Status
from respond import respond, error
from notify import publish, Topic

def handler(event, context):
    """
    payment handler
    """
    if 'operation' not in event:
        print('No operation specified')

    if event['operation'] == 'charge':
        #get charge result
        charge_result = create_charge(event)

        #publish here
        publish(charge_result, Topic.PAYMENT)

    else:
        print('Unknown operation')
