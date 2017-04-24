"""
Poll order-create queue and update db
"""

from dao import Dao, UnknownDbException
import json
import boto3

class Queue:
    """
    order-create queue url
    """
    URL = \
        'https://sqs.us-east-1.amazonaws.com/908762746590/order-created-queue'
    WAIT_TIME_S = 5
    MAX_MESSAGES = 10

def update_orders(event=None):
    """
    poll queue and update database
    """
    client = boto3.client('sqs')

    response = client.receive_message(
        QueueUrl=Queue.URL,
        AttributeNames=['All'],
        WaitTimeSeconds=Queue.WAIT_TIME_S,
        MaxNumberOfMessages=Queue.MAX_MESSAGES)

    if 'Messages' not in response:
        return

    # process messages
    messages = response['Messages']
    processed_messages = list()

    for message in messages:
        payload = json.loads(message['Body'])
        order_update = json.loads(payload['Message'])

        try:
            order_id = order_update['order_id']
            redirect_url = order_update['order_url']
            uid = order_update['uid']

            item = {
                'order_id': order_id,
                'uid': uid,
                'redirect_url': redirect_url
            }

            # overwrite items
            Dao.update_item(item)

            # append to processed list
            _processed = {
                'Id': message['MessageId'],
                'ReceiptHandle': message['ReceiptHandle']
            }

            processed_messages.append(_processed)

        except UnknownDbException as err:
            print(err)
        except Exception as err:
            # try upto 3 times and then reject
            print(err)

    #batch delete all messages
    if len(processed_messages) > 0:
        client.delete_message_batch(QueueUrl=Queue.URL,
                                    Entries=processed_messages)
