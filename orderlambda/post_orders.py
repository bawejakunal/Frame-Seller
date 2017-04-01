from __future__ import print_function

import pymysql
import datetime
from utils import Response, respond, get_mysql_connection, create_order_query

def post_order_details(event):
    """
    Future Enhancement: verify product info is correct
    """
    # Get parameters for creating order
    userid = event["uid"]
    product = event["body"]["product"]
    p_status = int(event["body"]["paymentstatus"])
    stripe_token = event["body"]["stripe_token"]
    timestamp = event["body"]["orderdate"]
    # Getting UNIX timestamp and creating datetime
    orderdatetime = datetime.datetime.fromtimestamp(float(timestamp))
    # Format orderdate from datetime
    orderdate = orderdatetime.strftime('%Y-%m-%d %H:%M:%S')
    product_resturl = ""

    linkarray = product["links"]

    # Get product URL
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
        orderurl = { "href" : "https://" + event["host"] + "/" + event["stage"] + "/orders/" + str(orderid) }
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
