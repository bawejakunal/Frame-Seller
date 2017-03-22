"""
Order status modification
"""

import json
import boto3

def update(payload):
    """
    send payload to orderfunction
    """
    response = boto3.client('lambda').invoke(
        FunctionName='Orchestrator',
        InvocationType='Event', #do not wait for response
        LogType='None',
        Payload=json.dumps(payload))

    return response
