"""
user verification
"""
from __future__ import print_function
# import json
# import boto3
from error import error
from dao import Dao, UnknownDbException

# def send_email(email, verify_page, verification_token):
#     """
#     send verification email
#     """
#     payload = {
#         "uemail": email,
#         "vtoken": verification_token,
#         "verify_page": verify_page
#     }
#     response = boto3.client('lambda').invoke(
#         FunctionName='SendEmail',
#         InvocationType='Event',
#         LogType='None',
#         Payload=json.dumps(payload))

#     return response

def verify_customer(body):
    """
    verify customer email
    """
    if ('uemail' not in body) or\
        ('vtoken' not in body):
        return error(401, 'Invalid email or token')

    try:
        customer = Dao.get_item('email', body['uemail'])

        if customer is None:
            return error(404, 'Customer does not exist')

        # user retrieved from database
        _verification = customer['verification']
        if customer['info']['verified'] == True:
            return error(400, 'Email already verified!')

        #verify email token
        elif _verification['token'] == body['vtoken']:
            try:
                #update item key, val and attr, value
                response = Dao.update_item('email', body['uemail'],
                                           'info.verified', True)
                verification_response = {
                    'success': True,
                    'message': 'Email verified'
                }
                return verification_response

            except UnknownDbException as err:
                return error(500, 'Unable to update customer information')
        else:
            return error(401, 'Email verification failed!')

    except UnknownDbException as err:
        return error(500, 'Unable to fetch customer information')
