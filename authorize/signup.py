"""
User module to signup user
"""
import os
import re
import uuid
from error import error
# from verify import send_email
from dao import Dao, AlreadyExistException, UnknownDbException
from notify import Topic, publish

EMAIL = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PASSWORD = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$")
def create_customer(body):
    """
    Create customer entry in table
    """

    #validate required entries
    if ('firstname' not in body) or\
        ('lastname' not in body) or\
        ('email' not in body) or\
        ('password' not in body) or\
        ('verify_page' not in body):
        return error(400, 'Missing parameters')

    #validate email and password regex
    if (EMAIL.match(body['email']) is None) or\
        (PASSWORD.match(body['password']) is None):
        return error(400, 'Invalid parameter')

    verification_token = os.urandom(16).encode('hex')

    try:
        #construct user item to insert in database
        user = {
            'uid': str(uuid.uuid4()),
            'email': body['email'].strip(),
            'password': body['password'],
            'info': {
                'firstname': body['firstname'].strip(),
                'lastname': body['lastname'].strip(),
                'active': True,
                'verified': False
            }
        }

        #add user entry to database through data abstraction
        Dao.put_item(user)

    except AlreadyExistException as err:
        return error(400, 'User already exists')
    except UnknownDbException as err:
        return error(500, 'Error creating user entry')
    else:

        """
        publish customer to customer-create topic
        IMPORTANT: remove hashed password before sending!
        """
        del user['password']
        payload = user
        payload['verify_page'] = body['verify_page'].strip()
        response = publish(payload, Topic.CUSTOMER_CREATE)

        return {
            'success': True,
            'message': 'Customer signup successful'
        }
