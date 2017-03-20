from __future__ import print_function

import boto3
from responses import Response, respond
from get_orders import get_order_details

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
        return respond(response_json, RESPONSE_BAD)

    if method == "GET":
        # execute the GET order code
        return get_order_details(event)

    elif method == "POST":
        # Handle post request
        print(event)
        respond(event, RESPONSE_INT_SER_ERR)
        """product = Product.objects.get(pk=product_id)
        try:
            charge = stripe.Charge.create(
                amount=int(product.price*100),
                currency="usd",
                metadata={"order_id": order_id},
                source=stripe_token)"""
        pass
    elif method == "PUT":
        # Handle put request
        pass