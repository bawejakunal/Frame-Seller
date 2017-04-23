from __future__ import print_function

import pymysql
import datetime
from validator import validate_json
from utils import Response, respond, get_mysql_connection, create_order_query, Payment
from dao import Dao, AlreadyExistException, UnknownDbException
from error import error

def create_order(payload):
    """
    Future Enhancement: verify product info is correct
    """
    # Get parameters for creating order

    if not validate_json(payload):
        return [False, 'Invalid JSON']

    event = payload['event']
    order_id = payload['order_id']
    userid = event['principal-id']
    host = event['host']
    stage = event['stage']
    protocol = event['proto']

    product = payload['data']['product']
    payment_status = Payment.UNPAID
    stripe_token = payload['data']['stripe_token']

    # Getting UNIX timestamp and creating datetime
    orderdatetime = datetime.datetime.utcnow()

    # Format orderdate from datetime
    order_date = orderdatetime.strftime('%Y-%m-%d %H:%M:%S')
    product_resturl = ""

    linkarray = product["links"]

    # Get product URL
    for links in linkarray:
        if links["rel"] == "self":
            product_resturl = links["href"]
            break

    err = False

    try:
        # construct user item to insert in database
        order_data = {
            'order_id': order_id,
            'order_date': order_date,
            'stripe_token': stripe_token,
            'payment_status':payment_status,
            'order_amount': product['price'],
            'product_url':product_resturl,
            'user_id':userid
        }

        # add user entry to database through data abstraction
        Dao.put_item(order_data)

        order_data["order_url"] = protocol + "://" + host + "/" + stage + "/orders/" + order_id;

        return [True, order_data]

    except AlreadyExistException as err:
        return [False, 'Order already exists']
    except UnknownDbException as err:
        return [False, 'Error creating order entry']


    """try:
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
            return [True, response_json]"""