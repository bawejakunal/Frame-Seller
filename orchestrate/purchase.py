"""
purchase order
"""
from __future__ import print_function
import json
from orders import create_order
from payment import Status, process_payment

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

        # async payment processing via adapter lambda
        response = process_payment(order_data)

        #overwrite data statusCode as 202
        #File aws lambda bug, it should be statusCode NOT StatusCode
        #wasted 10 mins of my life here :(
        data['statusCode'] = response['StatusCode']

    return data
