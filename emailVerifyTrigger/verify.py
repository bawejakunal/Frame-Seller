from __future__ import print_function
import json
from subscribe import Subscription
import boto3

emailVerifyStateMachineArn='arn:aws:states:us-east-1:908762746590:stateMachine:EmailVerify'

def email_verify(event, context):
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
            client = boto3.client('stepfunctions')
            response = client.start_execution(
                stateMachineArn= emailVerifyStateMachineArn,
                input=json.dumps(payload)
            )
            print(response)
