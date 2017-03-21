from __future__ import print_function

import pymysql
import datetime
from utils import Response, respond, get_mysql_connection, create_order_query
from hateoas import hateoas_constraints

def post_order_details(event):
    """
    Future Enhancement: verify product info is correct
    """
    userid = event["uid"]
    product = event["body"]["product"]
    p_status = int(event["body"]["paymentstatus"])
    stripe_token = event["body"]["stripe_token"]
    timestamp = event["body"]["orderdate"]
    orderdatetime = datetime.datetime.fromtimestamp(float(timestamp))
    orderdate = orderdatetime.strftime('%Y-%m-%d %H:%M:%S')
    product_resturl = ""

    linkarray = product["links"]

    for links in linkarray:
        if links["rel"] == "self":
            product_resturl = links["href"]
            break

    err = False
    err_code = Response.INT_SER_ERR

    try:
        conn = get_mysql_connection()
    except Exception as error:
        print(error.message)
        response_json = {"message": "System is facing some issues. Please try again later."}
        return respond(response_json, Response.INT_SER_ERR)

    try:
        cur = conn.cursor()
        query = create_order_query()

        cur.execute(query, (orderdate, stripe_token, p_status, int(product["id"]),
                            product_resturl, product["price"], userid))

        orderid = int(cur.lastrowid)
        orderurl = hateoas_constraints(True, event["host"], event["stage"], "/orders/", orderid)
        cur.connection.commit()

        response_json = { "orderid" : orderid, "orderurl" : orderurl }
    except Exception as error:
        print(error.message)
        err = True
        #use default error code
        response_json = { "message" : "System error. Please try later."}

    finally:
        cur.close()
        conn.close()
        if err:
            return respond(response_json, err_code)
        else:
            return respond(response_json, Response.OK)

        return respond(response_json, Response.OK)
