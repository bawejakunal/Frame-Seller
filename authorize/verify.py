"""
user verification
"""
from __future__ import print_function

import re
import json

from error import error
from dao import Dao, UnknownDbException
from jwtoken import verify_jwt
from signup import Role
import boto3

CLAIMS = {
    '^/orders(/)?$': ['GET'],
    '^/orderqueue(/)?$': ['GET'],
    '^/purchase(/)?$': ['POST'],
    '^/products(/)?(.)*$': ['GET']
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


def verify_resource_access(user_info, resource):
    """
    query database and check
    """
    payload = {
        'operation': 'verify',
        'uid': user_info['uid'],
        'resource': resource
    }
    response = invoke_order_lambda(payload, 'access-lambda')
    data = json.loads(response['Payload'].read())
    return data


def verify_access(user_info, verb, resource):
    """
    verify resource access for given customer role
    """

    # role verification
    if 'role' not in user_info or user_info['role'] != Role.CUSTOMER:
        return False

    _resource = resource.rstrip('/') #avoid trailing slash
    # allow access if resource in claims sent to user
    # match by regex
    for regex in CLAIMS:
        if re.match(regex, _resource) is not None:
            return verb in CLAIMS[regex]

    return verify_resource_access(user_info, _resource)


def invoke_order_lambda(payload, FunctionName=None, invoke='RequestResponse'):
    """
    invoke order lambda
    """
    response = boto3.client('lambda').invoke(
        FunctionName=FunctionName,
        InvocationType=invoke,
        LogType='None',
        Payload=json.dumps(payload))

    return response
