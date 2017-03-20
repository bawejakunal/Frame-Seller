"""
purchase order
"""
from __future__ import print_function
import boto3
import json
from lib.async_promises import Promise
import orders
from payment import create_charge

def buy_product(event, context):
    """
    Create database entry for order
    """
    response = orders.order(event, context)
    data = json.loads(response['Payload'].read())

    #if order accepted successfully
    #create payment asynchronously
    if int(data['statusCode']) == 200:
        order_data = json.loads(data['body'])
        promise = Promise(lambda resolve, reject:
                          reject(Exception('Payment Failed')\
                            if create_charge(order_data) is None else \
                            resolve('Payment Processed')))

        #process payment asynchronously
        promise.then(lambda result: print(result)).\
        catch(lambda error: print(error))

    return data
