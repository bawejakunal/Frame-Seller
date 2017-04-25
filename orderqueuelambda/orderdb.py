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
                'href': product['links'][0]['href'],
                'rel': 'order.product'
            }]
        }

        #add user entry to database through data abstraction
        Dao.put_item(order_data)

        self_link = {
            'href': construct_url(body['event'], order_data['order_id']),
            'rel': 'self'
        }
        order_data['links'] = [self_link] + order_data['links']

        #return order_id on successful put
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
        params = event['params']['path']

        # construct HATEOAS response            
        proto = event['params']['header']['CloudFront-Forwarded-Proto']
        host = event['params']['header']['Host']
        stage = event['context']['stage']
        path = event['context']['resource-path'].split('/')[1] #ign path params
        queue_url = '%s://%s/%s/%s' % (proto, host, stage, path)

        if 'orderid' in params:
            order_id = params['orderid']
            query_dict = {
                'order_id': order_id,
                'uid': uid
            }
            order = Dao.get_item(query_dict)

            # add hateoas url before sending
            if order is not None:
                if 'links' not in order:
                    order['links'] = list()

                order_url = "%s/%s" % (queue_url, order['order_id'])
                order_link = {'rel':'self', 'href':order_url}
                order['links'] = [order_link] + order['links']

            return order

        else:
            query_dict = {
                'uid': uid
            }
            query = Dao.query(query_dict)

            # HATEOAS response
            response = {
                'links':[
                {
                    'rel': 'orders.queue',
                    'href': queue_url
                }],
                'orders':list()
            }

            # add order links for HATEOAS compliance
            for order in query:
                if 'links' not in order:
                    order['links'] = list()
                order_url = "%s/%s" % (queue_url, order['order_id'])
                order_link = {
                    'href': order_url,
                    'rel': 'self'
                }
                order['links'] = [order_link] + order['links']
                response['orders'].append(order)

            return response

    except UnknownDbException as err:
        return error(500, "Error fetching order queue items")
    except KeyError:
        return error(400, "Invalid request")
