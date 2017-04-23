"""
Add or update order database items
"""
import uuid
from error import error
from dao import Dao, AlreadyExistException, UnknownDbException

def add_order(body):
    """
    add order to database
    """

    uid = body['event']['principal-id']
    order = dict(body['data'])

    try:
        #construct user item to insert in database
        order_data = {
            'order_id': str(uuid.uuid4()),
            'uid': uid,
            'info': order
        }

        #add user entry to database through data abstraction
        Dao.put_item(order_data)

        #return oid on successful put
        return order_data['order_id']

    except AlreadyExistException as err:
        return error(400, 'Order already exists')
    except UnknownDbException as err:
        return error(500, 'Error creating user entry')

def construct_url(event, order_id):
    """
    construct order url for polling
    """
    try:
        url = "%s://%s/%s/%s/%s" % (event['proto'], event['host'],
                                    event['stage'], 'orderqueue',
                                    str(order_id))
        return url
    except (KeyError, ValueError, TypeError) as err:
        return ''

def order_queue(event):
    """
    query queue db based on event structure
    """

    try:
        uid = event['context']['authorizer-principal-id']
        path = event['params']['path']
        if 'orderid' in path:
            order_id = path['orderid']
            query_dict = {
                'order_id': order_id,
                'uid': uid
            }
            order = Dao.get_item(query_dict)
            if order is None:
                return error(404, "No order found")
            return order

        else:
            return (500, "Not Implemented")

    except KeyError:
        return error(400, "Invalid request")
