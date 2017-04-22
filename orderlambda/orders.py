from __future__ import print_function

from utils import Response, respond, get_mysql_connection
from get_orders import get_order_details
from create_orders import create_order
from put_orders import put_order_details
from subscribe import Subscription, Queue
from error import error
from notify import Topic, publish
import boto3
import json

print('Loading orders function')

def order_handler(event, context):
    '''
        Handles : GET and POST request
        /GET Request:
            /orders -> Return all orders for the given user.
            /orders/{orderid} -> Return order with particular {orderid} if that order belongs to that user
        /POST Request:
            /orders -> Creates order with the given body JSON and returns 201 : Order created
    '''

    # If you have received an SNS notification, process here
    if "Records" in event:
        # Read from SNS messgage
        sns = event["Records"][0]["Sns"]
        topic_arn = sns["TopicArn"]

        # Discard all other messages
        if Subscription[topic_arn] == "order-update":
            payload = json.loads(sns["Message"])
            return put_order_details(payload)
    elif "context" in event:
        """
        For HTTP requests process here
        """

        valid_operations = ["GET"]
        method = event["context"]["http-method"]

        if method not in valid_operations:
            msg = "Bad Request"
            error(Response.BAD,msg)

        return get_order_details(event)
    
    elif 'detail-type' in event and event['detail-type'] == 'Scheduled Event':
        """
            order handler invoked by Cloudwatch event
            OrderSchedule
            """
        client = boto3.client('sqs')

        response = client.receive_message(
            QueueUrl=Queue.ORDER_QUEUE_URL,
            AttributeNames=['All'],
            WaitTimeSeconds=Queue.WAIT_TIME_S,
            MaxNumberOfMessages=Queue.MAX_MESSAGES)

        # ignore if no messages returned by queue
        if 'Messages' not in response:
            return

        # process messages
        messages = response['Messages']

        for message in messages:
            print(message)
            payload = json.loads(message['Body'])  # sqs message body

            if 'type' in payload and payload['type'] == 'create_order':
                status, response = create_order(payload)

                if status:
                    #write code to push to SQS
                    try:
                        response = publish(response, Topic.ORDER)

                        if response is not None:
                            response = client.delete_message(
                                QueueUrl=Queue.ORDER_QUEUE_URL,
                                ReceiptHandle=message['ReceiptHandle']
                            )

                    except:
                        print("Order creation failed, message will be visible in queue after Visibility timeout")

                else:
                    print("false")

            elif 'type' in payload and payload['type'] == 'update_order':
                pass