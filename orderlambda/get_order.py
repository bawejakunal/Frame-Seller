from __future__ import print_function

import boto3
import json
import sys
import os
import pymysql

print('Loading function')

valid_operations = ["GET"]

pay_status = {0: "UNPAID", 1: "PAID", 2: "FAILED"}


def get_payment_status(payment_code):
    return pay_status[payment_code]


def hateoas_constraints(userid, event, mul_order, host, stage, path, orderid=None):
    if orderid:
        if mul_order:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + path + str(orderid)}]
        else:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + path}]
    else:
        links = [{"rel": "orders.list", "href": "https://" + host + "/" + stage + path}]
    return links


def hateoas_product(producturl):
    return {"rel": "order.product", "href": producturl}


def hateoas_user(userid, event, host, stage):
    return {"rel": "order.user", "href": "https://" + host + "/" + stage + "/user/" + userid}


def respond(err, res):
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }


def order_handler(event, context):
    '''
        Handles : GET and POST request
        /GET Request:
            /orders -> Return all orders for the given user.
            /orders/{orderid} -> Return order with particular {orderid} if that order belongs to that user
        /POST Request:
            /orders -> Creates order with the given body JSON and returns 201 : Order created
    '''
    response_json = {}
    err = False
    method = event["httpMethod"]
    host = event["host"]
    stage = event["stage"]
    path = event["path"]

    if method not in valid_operations:
        err = "{ \"error\" : \"Not supported method\" }"
        return respond(err)

    rds_dbname = os.environ['dbname']
    rds_username = os.environ['dbusername']
    rds_password = os.environ['dbpassword']
    rds_host = os.environ['dbhost']
    rds_port = int(os.environ['dbport'])

    path_parameters = event["pathParameters"]
    userid = event["uid"]

    if method == "GET":
        # execute the GET order code

        # return all orders
        if path_parameters is None:
            order_list = []
            try:
                conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password,
                                       db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
            except:
                err = True
                response_json = {"error": "System is facing some issues. Please try again later."}
                return respond(err, response_json)
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "select id, product_id, product_url, user_id, paymentstatus, orderdate from " + os.environ[
                            'tablename_order'] + " where user_id = '" + userid + "'")
                    for order in cur:
                        orderdatetime = order["orderdate"]
                        order["orderdate"] = orderdatetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                        order["paymentstatus"] = get_payment_status(order["paymentstatus"])
                        order["links"] = hateoas_constraints(userid, event, True, host, stage, path, order["id"])
                        order["links"].append(hateoas_product(order["product_url"]))
                        order["links"].append(hateoas_user(userid, event, host, stage))
                        del order['user_id']
                        del order['product_url']
                        order_list.append(order)

                response_json["orders"] = order_list
                response_json["links"] = hateoas_constraints(userid, event, True, host, stage, path)
            except:
                err = True
                response_json = {"error": "Invalid order"}
            finally:
                cur.close()
                conn.close()
                resp = respond(err, response_json)
                print("Response")
                print(resp)
                return resp

        # if there is orderid in path parameters, return that particular order
        elif path_parameters is not None and "orderid" in path_parameters:
            orderid = path_parameters["orderid"]
            # get order from db having that orderid
            order = None

            try:
                conn = pymysql.connect(host=rds_host, port=rds_port, user=rds_username, passwd=rds_password,
                                       db=rds_dbname, connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
            except:
                err = True
                response_json = {"error": "System is facing some issues. Please try again later."}
                return respond(err, response_json)
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "select id, product_id, user_id, product_url, paymentstatus, orderdate from " + os.environ[
                            'tablename_order'] + " where user_id = '" + userid + "' AND id = " + orderid)
                    if cur.rowcount == 0:
                        err = True
                        response_json = {"error": "Invalid request"}
                    for row in cur:
                        order = row
                        orderdatetime = order["orderdate"]
                        order["orderdate"] = orderdatetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                        order["paymentstatus"] = get_payment_status(order["paymentstatus"])
                        order["links"] = hateoas_constraints(userid, event, False, host, stage, path, order["id"])
                        order["links"].append(hateoas_product(order["product_url"]))
                        order["links"].append(hateoas_user(userid, event, host, stage))
                        del order['user_id']
                        del order['product_url']

                response_json = order
            except:
                err = True
                err = {"error": " Invalid order"}
            finally:
                cur.close()
                conn.close()
                return respond(err, response_json)

    elif method == "POST":
        # Handle post request
        pass
    else:
        err = "{ \"error\" : \" Invalid request\"}"
        return respond(err)