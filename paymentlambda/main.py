"""
handle payment processing
"""
import json
from payment import create_charge
from notify import publish, Topic
from subscribe import Subscription

def handler(event, context):
    """
    payment handler
    """

    #process SNS invoke
    #ignore non sns invokes
    if 'Records' in event:
        sns = event['Records'][0]['Sns']
        topic_arn = sns['TopicArn']

        #new order arrives, create payment else ignore
        if Subscription[topic_arn] == 'order':
            payload = json.loads(sns['Message'])
            charge_result = create_charge(payload)
            publish(charge_result, Topic.PAYMENT)
