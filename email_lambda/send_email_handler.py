from __future__ import print_function
import json
from subscribe import Subscription

def send_email_handler(event, context):
    print(event)
    """
    send verification email
    """

    #drop all other requests
    if 'Records' in event:
        sns = event['Records'][0]['Sns']
        topic_arn = sns['TopicArn']

        #send email for verifcation
        if Subscription[topic_arn] == 'customer-create':
            payload = json.loads(sns['Message'])
