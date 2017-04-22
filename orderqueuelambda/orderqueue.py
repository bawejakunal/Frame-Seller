from __future__ import print_function

import boto3
import json

def orderqueue_handler(event, context):

    if 'context' in event and 'http-method' in event['context']:
        """
            This is an HTTP Method
        """
        method = event['context']['http-method']

        # get order details from dynamo db and send it back
        return
