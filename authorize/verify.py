"""
user verification
"""
from __future__ import print_function
from error import error
from dao import Dao, UnknownDbException
from jwtoken import verify_jwt
from signup import Role

CLAIMS = {
    '/orders': ['GET'],
    '/orderqueue': ['GET'],
    '/purchase': ['POST'],
    '/products': ['GET']
}

def verify_customer(body):
    """
    verify customer email
    """
    if 'verify_token' not in body:
        return error(400, 'Missing verification token')

    _jwt_payload = verify_jwt(body['verify_token'])

    if _jwt_payload is None:
        return error(401, 'Invalid token')

    #extract user email from jwt
    email = _jwt_payload['email']

    try:
            #update item key, val and attr, value
        response = Dao.update_item('email', email,
                                   'info.verified', True)
        verification_response = {
            'success': True,
            'message': 'Email verified'
        }

        return verification_response

    except UnknownDbException as err:
        return error(500, 'Unable to update customer information')


def verify_resource_access(resource, verb, user_info):
    """
    query database and check
    """
    print(resource)
    print(user_info)
    print(verb)
    return True


def verify_access(user_info, verb, resource):
    """
    verify resource access for given customer role
    """

    # role verification
    if 'role' not in user_info or user_info['role'] != Role.CUSTOMER:
        return False

    # allow access if resource in claims sent to user
    if resource in CLAIMS and verb in CLAIMS[resource]:
        return True

    return verify_resource_access(user_info, verb, resource)
