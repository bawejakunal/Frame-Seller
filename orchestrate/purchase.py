"""
purchase order
"""
from __future__ import print_function
import json
from orders import create_order
from payment import Status

def buy_product(event):
    """
    Create order entry with unpaid status
    """
    body = json.loads(event['body'])
    data = create_order(event, Status.UNPAID)

    #if order accepted successfully
    #create payment asynchronously
    #return 202 accepted response to user
    if int(data['statusCode']) == 200:
        order_data = json.loads(data['body'])
        order_data['stripe_token'] = body['stripe_token']
        order_data['price'] = body['product']['price']

        #TODO: invoke async lambda or push to SNS for
        #payment processing

    return data
