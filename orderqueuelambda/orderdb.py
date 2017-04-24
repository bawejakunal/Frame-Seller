"""
Add or update order database items
"""
import uuid
from error import error
from dao import Dao, AlreadyExistException, UnknownDbException

def add_order(event):
    """
    add order to database
    """

    body = event['body-json'].copy()

    #create order info
    order_id = str(uuid.uuid4())
    uid = body['event']['principal-id']
    url = construct_url(body['event'], order_id)

    #extract order info
    order = dict(body['data'])
    product = order['product']

    try:
        #construct order item to insert in database
        order_data = {
            'order_id': order_id,
            'uid': uid,
            'price': product['price'],
            'links': [{
                'href': url,
                'rel': 'self'
            }, {
                'href': product['links'][0]['href'],
                'rel': 'order.product'
            }]
        }

        #add user entry to database through data abstraction
        Dao.put_item(order_data)

        #return oid on successful put
        return order_data

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
            return order
        else:
            query_dict = {
                'uid': uid
            }
            query = Dao.query(query_dict)
            return query

    except UnknownDbException as err:
        return error(500, "Error fetching order queue items")
    except KeyError:
        return error(400, "Invalid request")
