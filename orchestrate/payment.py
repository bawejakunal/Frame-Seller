"""
Payment processing module
"""
import boto3
import json

class Status:
    """
    Describe payment status
    """
    UNPAID = 0
    PAID = 1
    FAILED = 2

def process_payment(order_data):
    """
    process payment through adapter lambda
    """

    payload = {
        'operation': 'charge',
        'order': order_data
    }

    #async call to lambda
    response = boto3.client('lambda').invoke(
        FunctionName='payments',
        InvocationType='Event',
        LogType='None',
        Payload=json.dumps(payload))

    return response
