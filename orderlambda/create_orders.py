from __future__ import print_function

import pymysql
import datetime
from validator import validate_json
from utils import Response, respond, get_mysql_connection, create_order_query, Payment

def create_order(payload):
    """
    Future Enhancement: verify product info is correct
    """
    # Get parameters for creating order
    if not validate_json(payload):
        return [False, 'Invalid JSON']

    event = payload['event']
    userid = event['principal-id']
    host = event['host']
    stage = event['stage']
    protocol = event['proto']

    product = payload['data']['product']
    p_status = Payment.UNPAID
    stripe_token = payload['data']['stripe_token']
    # Getting UNIX timestamp and creating datetime
    orderdatetime = datetime.datetime.utcnow()
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

    try:
        conn = get_mysql_connection()
    except Exception as error:
        print(error.message)
        response_json = {"error_code":Response.INT_SER_ERR ,"message": "System is facing some issues. Please try again later."}
        return [False, response_json]

    try:
        cur = conn.cursor()
        query = create_order_query()

        cur.execute(query, (orderdate, stripe_token, p_status, int(product["id"]),
                            product_resturl, product["price"], userid))

        orderid = int(cur.lastrowid)
        orderurl = { "href" : protocol+"://" + host + "/" + stage + "/orders/" + str(orderid) }
        cur.connection.commit()

        response_json = { "orderid" : orderid, "orderurl" : orderurl, "stripe_token":stripe_token, "price":product["price"] }
    except Exception as error:
        print(error.message)
        err = True
        response_json = {"error_code": Response.INT_SER_ERR,
                         "message": "System is facing some issues. Please try again later."}

    finally:
        cur.close()
        conn.close()
        if err:
            return [False,response_json]
        else:
            return [True, response_json]