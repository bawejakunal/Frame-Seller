"""
Publish payment to SNS topic
"""

import boto3
import json


"""
PAYMENT SNS TOPIC
"""
SNS_CLIENT = boto3.client('sns')

class Topic:
    """
    List of SNS topics
    """
    PAYMENT = "payment"

def publish(message, topic):
    """
    publish message to sns topic
    """

    #Idempotent topic creation
    #returns a dict containing topic arn
    _sns_topic = SNS_CLIENT.create_topic(Name=topic)
    _arn = _sns_topic['TopicArn']
    return SNS_CLIENT.publish(
        TopicArn=_arn,
        Message=json.dumps(message))
