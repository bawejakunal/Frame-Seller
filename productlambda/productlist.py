# -*- coding: utf-8 -*-
from __future__ import print_function
from responses import Response,respond
from get_product_details import get_product_details
import json
from error import error

valid_operations = ["GET"]

def product_handler(event, context):
    '''
        Handles: GET request
        /GET Request:
            /products -> Return all products
            /products/{productid} -> Return product with particular {productid}
    '''
    print(event)
    valid_operations = ["GET"]
    method = event["context"]["http-method"]

    if method not in valid_operations:
        msg = "Not supported method"
        error(Response.BAD, msg)

    if method == "GET":
        return get_product_details(event)
    elif method == "POST":
        pass
    elif method=="PUT":
        pass