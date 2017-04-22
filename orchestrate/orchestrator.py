"""
Lamdba Orchestrator
"""

from __future__ import print_function
import json
from order import accept, validate
from error import error
from subscribe import Subscription
from notify import Topic, publish

def handler(event, context):
    """
    delegate work
    """
    try:
        print(event)
        #process SNS messages here
        if 'Records' in event:
            sns = event['Records'][0]['Sns']
            topic_arn = sns['TopicArn']

            #publish order update to on receiving payment
            if Subscription[topic_arn] == 'payment':
                payload = json.loads(sns['Message'])
                response = publish(payload, Topic.ORDER_UPDATE)
            else:
                print('Subscribed topic %s not implemented' % topic_arn)

        elif event['operation'] == 'purchase':
            order_data = event['body-json']
            if validate(order_data) is False:
                return error(400, "Malformed data")

            # add to sqs and intermediate database
            # extract order context from event
            response = accept(event, order_data)
            return response #map this to 202 accepted response

        else:
            return error(500, "Unknown operation")

    except KeyError as err:
        print(err)
        return error(400, "No resource specified")
