"""
purchase order
"""
from __future__ import print_function
import json
from orders import create_order
from payment import Status
from notify import publish, Topic
from botocore.exceptions import ClientError

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

        # publish new order
        # topic name = 'order'
        try:
            response = publish(order_data, Topic.ORDER)
            if response is not None:
                data['statusCode'] = 202
                data['headers'] = {
                    'Location': order_data['orderurl']['href']
                }
        except (ClientError, KeyError) as err:
            print(err)
            data['statusCode'] = 500
            data['headers'] = None

    return data
