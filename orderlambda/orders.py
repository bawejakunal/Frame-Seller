from __future__ import print_function

from utils import Response, respond, get_mysql_connection
from get_orders import get_order_details
from post_orders import post_order_details
from put_orders import put_order_details
from subscribe import Subscription
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
    else:
        """
        For HTTP requests process here
        """
        valid_operations = ["GET", "POST"]
        method = event["httpMethod"]

        if method not in valid_operations:
            response_json = { "error" : "Bad Request" }
            return respond(response_json, Response.BAD)

        if method == "GET":
            # execute the GET order code
            return get_order_details(event)
        elif method == "POST":
            # Handle post request
            return post_order_details(event)