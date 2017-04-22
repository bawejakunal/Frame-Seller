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

    uid = body['uid']
    order = body['order']

    try:
        #construct user item to insert in database
        order_data = {
            'oid': str(uuid.uuid4()),
            'uid': uid,
            'info': dict(order)
        }

        #add user entry to database through data abstraction
        response = Dao.put_item(order_data)
        return response

    except AlreadyExistException as err:
        return error(400, 'User already exists')
    except UnknownDbException as err:
        return error(500, 'Error creating user entry')
