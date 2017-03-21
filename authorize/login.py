"""
Create JWT Token for valid user login
"""

from __future__ import print_function

from jwtoken import create_jwt
import boto3
from error import error
from botocore.exceptions import ClientError
from dao import Dao, UnknownDbException

def validate_user(email, password):
    """
    Fetch only user infor from database
    """
    try:
        #get user from databse by 'email' key, value as email
        customer = Dao.get_item('email', email)

        #no customer found
        if customer is None:
            return error(404, 'Customer does not exist')

        #user retrieved from database
        _info = customer['info']

        #user not verified then unauthorize
        if not _info['verified']:
            return error(401, 'Customer not verified')

        #user deactivated then unauthorize
        if not _info['active']:
            return error(401, 'Customer de-activated')

        #TODO: hash passwords
        if customer['password'] == password:
            customer_info = {
                'uid': customer['uid'],
                'firstname': _info['firstname'],
                'lastname': _info['lastname'],
                'email': customer['email']
            }

        return customer_info

    except UnknownDbException as err:
        return error(500, 'Unable to fetch customer information')


def login_customer(body):
    """
    Customer authentication
    """
    if ('email' not in body) or\
        ('password' not in body):
        return error(401, 'Invalid credentials')

    customer_info = validate_user(body['email'], body['password'])

    if not customer_info:
        return error(401, 'Invalid credentials')

    #valid customer obtained now generate jwt token
    return create_jwt(customer_info)
