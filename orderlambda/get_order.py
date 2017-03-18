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
    
def hateoas_constraints(userid, event, mul_order, orderid = None):
    if orderid:
        if mul_order:
            links = [ { "rel":"self", "href": "https://"+event["headers"]["Host"]+"/"+event["requestContext"]["stage"]+ event["path"]+str(orderid) }]
        else:
            links = [ { "rel":"self", "href": "https://"+event["headers"]["Host"]+"/"+event["requestContext"]["stage"]+ event["path"] }]
    else:
        links = [ { "rel":"orders.list", "href": "https://"+event["headers"]["Host"]+"/"+event["requestContext"]["stage"]+ event["path"] }]
    return links
    
def hateoas_product(producturl):
    return { "rel":"order.product", "href": producturl}

def hateoas_user(userid, event):
    return { "rel":"order.user", "href": "https://"+event["headers"]["Host"]+"/"+event["requestContext"]["stage"]+ "/user/" + userid}

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
    print(event)
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
    userid = event["requestContext"]["authorizer"]["principalId"]
    
    # return all orders
    if path_parameters is None:
        order_list = []
        try:
            conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        except:
            err = "{ \"error\" : \"System is facing some issues. Please try again later.\"}"
            return respond(err)
        try:
            with conn.cursor() as cur:
                cur.execute("select id, product_id, product_url, user_id, paymentstatus, orderdate from "+ os.environ['tablename_order'] + " where user_id = '" + userid+"'")
                for order in cur:
                    orderdatetime = order["orderdate"]
                    order["orderdate"] = orderdatetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                    order["paymentstatus"] = get_payment_status(order["paymentstatus"])
                    order["links"] = hateoas_constraints(userid, event, True , order["id"])
                    order["links"].append(hateoas_product(order["product_url"]))
                    order["links"].append(hateoas_user(userid, event))
                    del order['product_id']
                    del order['user_id']
                    del order['product_url']
                    order_list.append(order)
                
            cur.close()
            conn.close()
            response_json["orders"] = order_list
            response_json["links"] = hateoas_constraints(userid, event, True)
            return respond(None, response_json)
        except:
            cur.close()
            conn.close()
            err = "{ \"error\" : \" Invalid order\" }"
            return respond(err)
    # if there is orderid in path parameters, return that particular order
    elif path_parameters is not None and "orderid" in path_parameters:
        orderid = path_parameters["orderid"]
        # get order from db having that orderid
        order = None

        try:
            conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        except:
            print("ERROR: Unexpected error: Could not connect to MySql instance.")
            sys.exit()
        try:
            with conn.cursor() as cur:
                cur.execute("select id, product_id, user_id, product_url, paymentstatus, orderdate from " + os.environ['tablename_order'] + " where user_id = '" + userid + "' AND id = " + orderid)
                if cur.rowcount == 0:
                    cur.close()
                    conn.close()
                    err = "{ \"error\" : \" Invalid order\"}"
                    return respond(err)
                for row in cur:
                    order = row
                    orderdatetime = order["orderdate"]
                    order["orderdate"] = orderdatetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                    order["paymentstatus"] = get_payment_status(order["paymentstatus"])
                    order["links"] = hateoas_constraints(userid, event, False, order["id"])
                    order["links"].append(hateoas_product(order["product_url"]))
                    order["links"].append(hateoas_user(userid, event))
                    del order['product_id']
                    del order['user_id']
                    del order['product_url']
            cur.close()
            conn.close()
            return respond(None, order)
        except:
            cur.close()
            conn.close()
            err = "{ \"error\" : \" Invalid order\"}"
            return respond(err)
    else:
        err = "{ \"error\" : \" Invalid request\"}"
        return respond(err)