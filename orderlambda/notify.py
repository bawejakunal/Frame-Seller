"""
Simple message publication
"""

import json
import boto3

"""
SNS wrapper
"""
SNS_CLIENT = boto3.client('sns')

class Topic(object):
    """
    List of SNS topics
    """
    ORDER = "order"

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