"""
Add or update order database items
"""
import uuid
import urlparse
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
            'oid': str(uuid.uuid4()),
            'uid': uid,
            'info': order
        }

        #add user entry to database through data abstraction
        response = Dao.put_item(order_data)
        return response

    except AlreadyExistException as err:
        return error(400, 'User already exists')
    except UnknownDbException as err:
        return error(500, 'Error creating user entry')

def construct_url(event, order_id):
    """
    construct order url for polling
    """
    url = event['proto'] + '://'
    url += event['host']
    url = urlparse.urljoin(url, event['stage'])
    url = urlparse.urljoin(url, str(order_id))
    return url
