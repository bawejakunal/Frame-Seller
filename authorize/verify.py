"""
user verification
"""
from __future__ import print_function
import os
import json
import boto3
from error import error
from botocore.exceptions import ClientError
from dao import Dao, UnknownDbException

def send_email(email, verification_token):
    """
    send verification email
    """
    payload = {
            "uemail": email,
            "vtoken": verification_token
    }
    response = boto3.client('lambda').invoke(
        FunctionName='SendEmail',
        InvocationType='Event',
        LogType='None',
        Payload=json.dumps(payload))

    return response

    # try:
    #     aws_access_key_id = os.environ['LOCAL_AWS_ACCESS_KEY']
    #     aws_secret_access_key = os.environ['LOCAL_AWS_SECRET_KEY']
    #     email_client = boto3.client('ses', aws_access_key_id=aws_access_key_id,
    #                                 aws_secret_access_key=aws_secret_access_key
    #                                )
    #
    #     s3url = 'https://xyz.com/'
    #
    #     verification_url = (s3url + '?vtoken=' + verification_token +
    #                        '&uemail='+email)
    #
    #     response = email_client.send_email(
    #         Source='akshay2626@gmail.com',
    #         Destination={
    #             'ToAddresses': [
    #                 email,
    #             ],
    #             'BccAddresses': [
    #             ],
    #             'CcAddresses': [
    #             ],
    #         },
    #         Message={
    #             'Subject': {
    #                 'Data': 'Frameseller Email Verification',
    #                 'Charset': 'UTF-8'
    #             },
    #             'Body': {
    #                 'Text': {
    #                     'Data': 'Use this url to verify:'+verification_url,
    #                     'Charset': 'UTF-8'
    #                 },
    #                 'Html': {
    #                     'Data': 'Use <a href="'+verification_url+'">this url </a>to verify.',
    #                     'Charset': 'UTF-8'
    #                 }
    #             }
    #         },
    #         ReplyToAddresses=[
    #             'akshay2626@gmail.com',
    #         ],
    #     )
    # except ClientError as email_err:
    #     print(email_err.response)
    #     return error(500, 'Error sending email')
    #     # email config END
    #

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
