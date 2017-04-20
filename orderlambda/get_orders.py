from __future__ import print_function

import pymysql
from utils import Response, respond, get_mysql_connection, get_order_query
from hateoas import hateoas_constraints, hateoas_product#, hateoas_user
from error import error

pay_status = {0: "UNPAID", 1: "PAID", 2: "FAILED"}

def get_payment_status(payment_code):
    return pay_status[payment_code]

def get_json(order, userid, host, stage, path, mul_order):
    orderdatetime = order["orderdate"]
    order["orderdate"] = orderdatetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    order["paymentstatus"] = get_payment_status(order["paymentstatus"])
    order["links"] = hateoas_constraints(mul_order, host, stage, path, order["id"])
    order["links"].append(hateoas_product(order["product_url"]))
    #order["links"].append(hateoas_user(userid, host, stage))
    del order['user_id']
    del order['product_url']
    return order

def get_order_details(event):
    """
    Gets single or all orders for the given user
    """

    # Defining variables used through out the flow
    response_json = {}
    err = False
    error_code = Response.INT_SER_ERR

    print(event)
    path_parameters = event["params"]["path"]
    userid = event["context"]["authorizer-principal-id"]
    stage = event["context"]["stage"]
    path = event["context"]["resource-path"]
    host = event["params"]["header"]["Host"]


    if len(path_parameters.keys()) == 0:
        # If path_parameters is None, no orderid is specified and so return all orders
        order_list = []

        try:
            conn = get_mysql_connection()
        except:
            msg = "System is facing some issues. Please try again later."
            error(Response.INT_SER_ERR, msg)

        try:
            with conn.cursor() as cur:
                cur.execute(get_order_query(userid))

                for order in cur:
                    order = get_json(order, userid, host, stage, path, True)
                    order_list.append(order)

            response_json["orders"] = order_list
            response_json["links"] = hateoas_constraints(True, host, stage, path)
        except:
            err = True
            # Not setting error_code and using default
            msg = "System is facing some issues. Please try again later."
        finally:
            cur.close()
            conn.close()
            # Return error or valid json based on the condition.
            if err:
                error(error_code, msg)
            else:
                return response_json

    
    elif len(path_parameters.keys()) != 0 and "orderid" in path_parameters:
        # If path_parameters contains orderid information, return single order

        orderid = path_parameters["orderid"]
        # Get order from the DB having that orderid

        try:
            # Casting orderid to int to validate that orderid is correct and integer
            orderid = int(orderid)
        except ValueError:
            msg = "Bad Request"
            error(Response.BAD, msg)

        try:
            conn = get_mysql_connection()
        except:
            msg = "System is facing some issues. Please try again later."
            error(Response.INT_SER_ERR, msg)

        try:
            with conn.cursor() as cur:
                cur.execute(get_order_query(userid, orderid))

                """
                If cursor returns zero rows, it means that either such order doesn't exist
                or the user is not authorized to access this order.
                In either case we would be returning Forbidden response 
                as we don't want to reveal whether such order exists or not
                """
                if cur.rowcount == 0:
                    err = True
                    error_code = Response.FORBIDDEN
                    msg = "Not authorized to access this order"
                else:
                    for row in cur:
                        response_json = get_json(row, userid, host, stage, path, False)
        except:
            err = True
            #Not setting error_code and using default Response.INT_SER_ERR = '500'
            msg = "System is facing some issues. Please try again later."
        finally:
            cur.close()
            conn.close()
            # Return error or valid json based on the condition.
            if err:
                error(error_code, msg)
            else:
                return response_json
