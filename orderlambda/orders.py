from __future__ import print_function

from utils import Response, respond, get_mysql_connection
from get_orders import get_order_details
from post_orders import post_order_details
from put_orders import put_order_details

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
    valid_operations = ["GET", "POST", "PUT"]
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
    elif method == "PUT":
        # Handle put request
        return put_order_details(event)
        pass