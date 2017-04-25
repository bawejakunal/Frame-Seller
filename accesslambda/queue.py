"""
Poll queue and update dynamodb
"""

import json
import boto3
from dao import Dao, UnknownDbException

RESOURCE = {
    'arn:aws:sns:us-east-1:908762746590:order': '/orderqueue',
    'arn:aws:sns:us-east-1:908762746590:order-created': '/orders'
}

class Queue:
    """
    order-create queue url
    """
    URL = "https://sqs.us-east-1.amazonaws.com/908762746590/access-rule-queue"
    WAIT_TIME_S = 5
    MAX_MESSAGES = 10

def update_database(event):
    """
    update database
    """
    client = boto3.client('sqs')

    response = client.receive_message(
        QueueUrl=Queue.URL,
        AttributeNames=['All'],
        WaitTimeSeconds=Queue.WAIT_TIME_S,
        MaxNumberOfMessages=Queue.MAX_MESSAGES)

    if 'Messages' not in response:
        return

    messages = response['Messages']
    processed_messages = list()

    for message in messages:
        payload = json.loads(message['Body'])
        update = json.loads(payload['Message'])
        topic = payload['TopicArn']

        try:
            item = {'resource': RESOURCE[topic] + '/' + update['order_id']}

            if RESOURCE[topic] == '/orderqueue':
                item['uid'] = update['event']['principal-id']
            elif RESOURCE[topic] == '/orders':
                item['uid'] = update['uid']

            Dao.put_item(item)

            _processed = {
                'Id': message['MessageId'],
                'ReceiptHandle': message['ReceiptHandle']
            }

            processed_messages.append(_processed)

        except UnknownDbException as err:
            print(err)
        except Exception as err:
            print(err)

    if len(processed_messages) > 0:
        client.delete_message_batch(QueueUrl=Queue.URL,
            Entries=processed_messages)

