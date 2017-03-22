"""
User module to signup user
"""
import os
import uuid
import boto3
from error import error
from verify import send_email
from dao import Dao, AlreadyExistException, UnknownDbException

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
            },
            'verification':{
                'token': verification_token
            }
        }

        #add user entry to database through data abstraction
        Dao.put_item(user)

    except AlreadyExistException as err:
        return error(400, 'User already exists')
    except UnknownDbException as err:
        return error(500, 'Error creating user entry')
    else:
        # email config BEGIN
        email = body['email'].strip()
        verify_page = body['verify_page'].strip()
        send_email(email, verify_page, verification_token)

        return {
            'success': True,
            'message': 'Customer signup successful'
        }