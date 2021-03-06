from __future__ import print_function

from dao import Dao, UnknownDbException, AlreadyExistException
import datetime
from utils import Payment
from error import error
from validator import validate_json_createorder, validate_json_updatepayment


def create_order(payload):
    """
    Future Enhancement: verify product info is correct
    """
    # Get parameters for creating order

    if not validate_json_createorder(payload):
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
    order_date = orderdatetime.strftime('%Y-%m-%d %H:%M:%S UTC')
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
        order_url = protocol + "://" + host + "/" + stage + "/orders/" + order_id

        order_data = {
            'uid':userid,
            'order_id':order_id,
            'order_date': order_date,
            'stripe_token': stripe_token,
            'payment_status': payment_status,
            'order_amount': product['price'],
            'product_id': product['id'],
            'links':[
                {
                    'rel':'self',
                    'href': order_url
                },
                {
                    'rel': 'order.product',
                    'href': product_resturl
                }

            ]
        }

        # add user entry to database through data abstraction
        Dao.put_item(order_data)

        order_data["order_url"] = order_url
        return [True, order_data]

    except AlreadyExistException as err:
        return [False, 'Order already exists']
    except UnknownDbException as err:
        return [False, 'Error creating order entry']


def get_order(event):
    """
        Gets single or all orders for the given user
        """

    # Defining variables used through out the flow

    print(event)
    path_parameters = event["params"]["path"]
    userid = event["context"]["authorizer-principal-id"]
    stage = event["context"]["stage"].strip().strip('/')
    path = event["context"]["resource-path"].strip().strip('/')
    host = event["params"]["header"]["Host"].strip().strip('/')

    if len(path_parameters.keys()) == 0:
        # If path_parameters is None, no orderid is specified and so return all orders

        key_cond_exp = "uid = :uid"

        exp_attr_val = {':uid': userid}

        indexname ='order-date-index'

        orders = Dao.query(key_cond_exp, exp_attr_val, indexname=indexname)

        for order in orders:
            del order['stripe_token']

        response = {
            "orders": orders,
            "links": [
                {
                    'rel': 'orders.list',
                    'href': 'https://' + host + '/' + stage + '/' + path +'/'

                }
            ]
        }

        print(response)
        return response

    elif len(path_parameters.keys()) != 0 and "orderid" in path_parameters:
        # If path_parameters contains orderid information, return single order

        orderid = path_parameters["orderid"]

        query_dict = {
            'order_id': orderid,
            'uid': userid
        }
        order = Dao.get_item(query_dict)

        if order is None:
            raise error(404, 'Order Not Found')

        del order['stripe_token']
        
        print(order)

        return order


def update_order(payload):
    if not validate_json_updatepayment(payload):
        return [False, 'Invalid JSON']

    data = payload['data']

    try:
        key_dict = {
            'uid':data['uid'],
            'order_id':data['order_id']
        }

        update_exp = "SET payment_status = :new_status"

        exp_att_val_dict = {':new_status': data['payment_status']}

        Dao.update_item(key_dict, update_exp, exp_att_val_dict)
        return [True, "Order Updated"]
    except:
        return [False, "Couldn't update order"]

