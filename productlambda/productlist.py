# -*- coding: utf-8 -*-
from __future__ import print_function
import boto3
import json
import sys
import os
import pymysql

print('Loading function')

valid_operations = ["GET"]

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def product_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    method = event["httpMethod"]

    if method not in valid_operations:
        err = "{ \"error\" : \"Not supported method\" }" 
        return respond(err)

    rds_dbname = os.environ['dbname']
    rds_username = os.environ['dbusername']
    rds_password = os.environ['dbpassword']
    rds_host = os.environ['dbhost']
    rds_port = int(os.environ['dbport'])
    
    path_parameters = event["pathParameters"]
    
    #return all products
    if path_parameters is None:
        product_list =[]
        try:
            conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        except:
            print("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()
        with conn.cursor() as cur:
            cur.execute("select id, price, description, url from "+ os.environ['product_tablename'])
            for prd in cur:
                product_list.append(prd)
        print(product_list)
        return respond(None, product_list)
        
    # if there is productid in path parameters, return that particular product
    elif path_parameters is not None and "productid" in path_parameters:
        productid = path_parameters["productid"]
        # get order from db having that productid
        prd = None
        try:
            conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        except:
            print("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()
        try:
            with conn.cursor() as cur:
                cur.execute("select * from " + os.environ['product_tablename'] + " where id = " + productid)
                if cur.rowcount == 0:
                    err = "{ \"error\" : \"Invalid product\" }"
                    cur.close()
                    conn.close()
                    return respond(err)
                else:
                    for row in cur:
                        prd = row
                        cur.close()
                        conn.close()
                        return respond(None, prd)
        except:
            err = "{ \"error\" : \"Invalid product\" }"
            cur.close()
            conn.close()
            return respond(err)
            
            
    else:
        err = "Invalid product"
        return respond(err)