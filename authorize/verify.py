"""
user verification
"""
from __future__ import print_function
import os
import boto3
from error import error
from botocore.exceptions import ClientError

def send_email(email, verification_token):
    """
    send verification email
    """
    try:
        aws_access_key_id = os.environ['LOCAL_AWS_ACCESS_KEY']
        aws_secret_access_key = os.environ['LOCAL_AWS_SECRET_KEY']
        email_client = boto3.client('ses', aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key
                                   )

        s3url = 'https://xyz.com/'

        verification_url = (s3url + '?vtoken=' + verification_token +
                           '&uemail='+email)

        response = email_client.send_email(
            Source='akshay2626@gmail.com',
            Destination={
                'ToAddresses': [
                    email,
                ],
                'BccAddresses': [
                ],
                'CcAddresses': [
                ],
            },
            Message={
                'Subject': {
                    'Data': 'Frameseller Email Verification',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'Use this url to verify:'+verification_url,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': 'Use <a href="'+verification_url+'">this url </a>to verify.',
                        'Charset': 'UTF-8'
                    }
                }
            },
            ReplyToAddresses=[
                'akshay2626@gmail.com',
            ],
        )
    except ClientError as email_err:
        print(email_err.response)
        return error(500, 'Error sending email')
        # email config END


def verify_customer(body):
    """
    verify customer email
    """
    if ('uemail' not in body) or\
        ('vtoken' not in body):
        return error(401, 'Invalid email or token')

    customer_table = boto3.resource('dynamodb').Table('Customer')
    try:
        response = customer_table.get_item(
            Key={
                'email': body['uemail']
            }
        )
    except ClientError as err:
        print(err)
        return error(500, 'Unable to fetch customer information')
    else:
        if 'Item' not in response:
            return error(404, 'Customer does not exist')
        # user retrieved from database
        _item = response['Item']
        _verification = _item['verification']
        if _item['info']['verified'] == True:
            return error(400, 'Email already verified!')
        elif _verification['token'] == body['vtoken']:
            try:
                updateResponse = customer_table.update_item(
                    Key={
                        'email': body['uemail']
                    },
                    UpdateExpression="set info.verified = :x",
                    ExpressionAttributeValues={
                        ':x':True
                    },
                    ReturnValues="UPDATED_NEW"
                )
            except ClientError as err:
                print(err)
                return error(500, 'Unable to update customer verified information')
            else:
                verifiction_response = {
                    'success': True,
                    'message': 'Congrats! Your email has been verified successfully.'
                }
                return verifiction_response
        else:
            return error(401, 'Email verification failed!')
