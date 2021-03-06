"""
User module to signup user
"""
import os
import re
import uuid
from error import error
from jwtoken import create_jwt, TIME_DELTA
from dao import Dao, AlreadyExistException, UnknownDbException
from notify import Topic, publish

EMAIL = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PASSWORD = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$")

class Role:
    """
    User roles
    """
    CUSTOMER = "customer"


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
            'role': Role.CUSTOMER,
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
        _jwt_payload = {
            'email': user['email'],
            'uid': user['uid']
        }

        #24 hours jwt token expiry
        _jwt_token = create_jwt(_jwt_payload, 24 * TIME_DELTA)

        #subscribed services can verify jwt token with their key
        #send in user email verification mail from AWS Step function
        payload = dict()
        payload['email'] = user['email']
        payload['jwt'] = _jwt_token
        payload['uid'] = user['uid']
        payload['verify_page'] = body['verify_page'].strip()

        #publish the payload
        response = publish(payload, Topic.CUSTOMER_CREATE)
        print(response)
        print(payload)

        return {
            'success': True,
            'message': 'Customer signup successful'
        }
