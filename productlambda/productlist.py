# -*- coding: utf-8 -*-
from __future__ import print_function
from responses import Response,respond
from get_product_details import get_product_details
import boto3
import json
import sys
import os
import pymysql

print('Loading products function')

def product_handler(event, context):
    '''
        Handles: GET request
        /GET Request:
            /products -> Return all products
            /products/{productid} -> Return product with particular {productid}
    '''
    valid_operations = ["GET"]
    method = event["httpMethod"]

    if method not in valid_operations:
        err = "{ \"error\" : \"Not supported method\" }" 
        return respond(err, Response.BAD)

    if method == "GET":
        return get_product_details(event)
    elif method == "POST":
        pass
    elif method=="PUT":
        pass