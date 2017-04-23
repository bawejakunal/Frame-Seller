from __future__ import print_function

from utils import Response, respond, get_mysql_connection
from get_orders import get_order_details
from orders_op import create_order, update_order
from subscribe import Subscription, Queue
from error import error
from notify import Topic, publish
import boto3
import json

print('Loading orders function')

def order_handler(event, context):
    """
        Handles : GET and POST request
        /GET Request:
            /orders -> Return all orders for the given user.
            /orders/{orderid} -> Return order with particular {orderid} if that order belongs to that user
        /POST Request:
            /orders -> Creates order with the given body JSON and returns 201 : Order created
    """

    # If you have received an SNS notification, process here

    if "context" in event:
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
            payload = json.loads(message['Body'])  # sqs message body

            if 'Type' in payload and payload['Type'] == 'Notification' and 'Message' in payload: # check if the message from sqs in an SNS message

                sns_message = json.loads(payload['Message']) # Load message from SNS


                if 'type' in sns_message and sns_message['type'] == 'create_order': # Check if the message is of type 'create_order'
                    # Process Order

                    status, response = create_order(sns_message)

                    if status:
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
                        print("Order was not created")

                elif 'type' in sns_message and sns_message['type'] == 'update_payment':
                    print(sns_message)
                    status, response = update_order(sns_message)

                    if status:
                        print(response)
                        response = client.delete_message(
                            QueueUrl=Queue.ORDER_QUEUE_URL,
                            ReceiptHandle=message['ReceiptHandle']
                        )
                    else:
                        print(response)

                    return