"""
Lamdba Orchestrator
"""

from __future__ import print_function
import json
import orders
import purchase
from respond import respond, error
from subscribe import Subscription
from notify import Topic, publish

def handler(event, context):
    """
    delegate work
    """
    print(event)
    try:
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

        #handle API gateway invokes below
        elif event['resource'].startswith('/orders'):
            try:
                response = orders.order(event)
                data = json.loads(response["Payload"].read())
                body = json.loads(data['body'])
                return respond(data['statusCode'], body)
            except (KeyError, Exception) as err:
                #in case of unhandled exception
                print(err)
                return error(500, 'Error processing order request')

        elif event['resource'].startswith('/purchase'):
            status = None

            #create order and publish to topic
            data = purchase.buy_product(event)
            body = json.loads(data['body'])

            #return accepted with order url once
            #payment/order accepted for processing
            status = data['statusCode']
            headers = data['headers']
            return respond(status, body, headers)

        else:
            return error(500, "Unknown operation")

    except KeyError as err:
        print(err)
        return error(400, "No resource specified")
