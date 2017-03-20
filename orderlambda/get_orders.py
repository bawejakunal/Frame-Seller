from __future__ import print_function

import boto3
import os
import pymysql
from responses import Response, respond
from hateoas import hateoas_constraints, hateoas_product, hateoas_user

pay_status = {0: "UNPAID", 1: "PAID", 2: "FAILED"}

def get_payment_status(payment_code):
    return pay_status[payment_code]

def get_mysql_connection():
    rds_dbname = os.environ['dbname']
    rds_username = os.environ['dbusername']
    rds_password = os.environ['dbpassword']
    rds_host = os.environ['dbhost']
    rds_port = int(os.environ['dbport'])

    return pymysql.connect(host=rds_host, port=rds_port, 
                            user=rds_username, passwd=rds_password,
                            db=rds_dbname, connect_timeout=5,
                            cursorclass=pymysql.cursors.DictCursor)

def get_json(order, userid, host, stage, path):
    orderdatetime = order["orderdate"]
    order["orderdate"] = orderdatetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    order["paymentstatus"] = get_payment_status(order["paymentstatus"])
    order["links"] = hateoas_constraints(userid, True, host, stage, path, order["id"])
    order["links"].append(hateoas_product(order["product_url"]))
    order["links"].append(hateoas_user(userid, host, stage))
    del order['user_id']
    del order['product_url']
    return order

def get_order_query(userid, orderid=None):
    if orderid is None:
        return ("select id, product_id, product_url, user_id, paymentstatus,\
                orderdate from " + os.environ['tablename_order']
                + " where user_id = '" + userid + "'")
    else:
        return ("select id, product_id, user_id, product_url, paymentstatus, \
                orderdate from " + os.environ['tablename_order']
                + " where user_id = '" + userid + "' AND id = " + str(orderid))



def get_order_details(event):

    response_json = {}
    err = False
    error_code = Response.INT_SER_ERR

    path_parameters = event["pathParameters"]
    userid = event["uid"]
    stage = event["stage"]
    path = event["path"]
    host = event["host"]


    if path_parameters is None:
        # return all orders
        order_list = []

        try:
            conn = get_mysql_connection()
        except:
            response_json = {"error": "System is facing some issues. Please try again later."}
            return respond(response_json, Response.INT_SER_ERR)

        try:
            with conn.cursor() as cur:
                cur.execute(get_order_query(userid))

                for order in cur:
                    order = get_json(order, userid, host, stage, path)
                    order_list.append(order)

            response_json["orders"] = order_list
            response_json["links"] = hateoas_constraints(userid, True, host, stage, path)
        except:
            err = True
            #Not setting error_code and using default
            response_json = {"error": "System is facing some issues. Please try again later."}
        finally:
            cur.close()
            conn.close()
            if err: 
                return respond(response_json, error_code)
            else:
                return respond(response_json, Response.OK)

    # if there is orderid in path parameters, return that particular order
    elif path_parameters is not None and "orderid" in path_parameters:
        
        orderid = path_parameters["orderid"]
        # get order from db having that orderid

        try:
            orderid = int(orderid)
        except ValueError:
            response_json = {"error": "Bad Request"}
            return respond(response_json, Response.BAD)

        try:
            conn = get_mysql_connection()
        except:
            response_json = {"error": "System is facing some issues. Please try again later."}
            return respond(response_json, Response.INT_SER_ERR)

        try:
            with conn.cursor() as cur:
                cur.execute(get_order_query(userid, orderid))
                    
                if cur.rowcount == 0:
                    err = True
                    error_code = Response.FORBIDDEN
                    response_json = {"error": "Not authorized to access this order"}
                for row in cur:
                    response_json = get_json(row, userid, host, stage, path)
        except:
            err = True
            #Not setting error_code and using default Response.INT_SER_ERR = '500'
            response_json = {"error": "System is facing some issues.\
                                Please try again later."}
        finally:
            cur.close()
            conn.close()
            if err:
                return respond(response_json, error_code)
            else:
                return respond(response_json, Response.OK)