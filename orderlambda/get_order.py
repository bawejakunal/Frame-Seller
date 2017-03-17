from __future__ import print_function

import boto3
import json
import sys
import os
import pymysql

print('Loading function')

valid_operations = ["GET"]

pay_status = { 0 : "UNPAID", 1 :"PAID", 2 : "FAILED" }

def get_payment_status(payment_code):
    return pay_status[payment_code]
    
def hateoas_constraints(userid, event, orderid = None):
    if orderid:
        links = [ { "rel":"self", "href": "https://"+event["headers"]["Host"]+"/"+event["requestContext"]["stage"]+"/"+ event["path"] }]
    else:
        links = [ { "rel":"orders.list", "href": "https://"+event["headers"]["Host"]+"/"+event["requestContext"]["stage"]+"/"+ event["path"] }]
    return links 

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def order_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))
    response_json = {}

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
    userid = path_parameters["userid"]
    
    # return all orders
    if "orderid" not in path_parameters:
        order_list = []
        #try:
        conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        #except:
            #print("ERROR: Unexpected error: Could not connect to MySql instance.")
            #sys.exit()
    
        with conn.cursor() as cur:
            cur.execute("select id, product_id, user_id, paymentstatus, orderdate from "+ os.environ['tablename_order'] + " where user_id = " + userid)
            for order in cur:
                orderdatetime = order["orderdate"]
                order["orderdate"] = orderdatetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                order["paymentstatus"] = get_payment_status(order["paymentstatus"])
                order["links"] = hateoas_constraints(userid, event, order["id"])
                order_list.append(order)

        cur.close()
        conn.close()
        response_json["orders"] = order_list
        response_json["links"] = hateoas_constraints(userid, event)
        return respond(None, response_json)
    
    # if there is orderid in path parameters, return that particular order
    else:
        orderid = path_parameters["orderid"]
        # get order from db having that orderid
        order = None

        try:
            conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        except:
            print("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()
        with conn.cursor() as cur:
            cur.execute("select id, product_id, user_id, paymentstatus, orderdate from " + os.environ['tablename_order'] + " where user_id = " + userid + " AND id = " + orderid)
            for row in cur:
                order = row
                orderdatetime = order["orderdate"]
                order["orderdate"] = orderdatetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                order["paymentstatus"] = get_payment_status(order["paymentstatus"])
                order["links"] = hateoas_constraints(userid, event, order["id"])

        return respond(None, order)
   