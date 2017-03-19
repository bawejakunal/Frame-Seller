"""
User module to signup user
"""
import os

import boto3
from botocore.exceptions import ClientError
from error import error
import uuid

def create_customer(body):
    """
    Create customer entry in table
    """

    #validate required entries
    if ('firstname' not in body) or\
        ('lastname' not in body) or\
        ('email' not in body) or\
        ('password' not in body):
        return error(400, 'Missing parameters')

    #get the Customer table
    user_table = boto3.resource('dynamodb').Table('Customer')
    
    try:
        response = user_table.put_item(
            Item={
                'uid': str(uuid.uuid4()), #unique id of user
                'email': body['email'].strip(),
                'password' : body['password'],
                'info' : { #TODO: hash, salt
                    'firstname' : body['firstname'].strip(),
                    'lastname' : body['lastname'].strip(),
                    'active': True,
                    'verified' : True #TODO: email verification
                }
            },
            ConditionExpression="attribute_not_exists(uid) AND attribute_not_exists(email)"
        )

    except ClientError as err:
        if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return error(400, 'User already exists')
        else:
            print(err.response)
        return error(500, 'Error creating user entry')

    else:
        # email config BEGIN
        try:
            email_client = boto3.client('ses',
                                        aws_access_key_id=os.environ['LOCAL_AWS_ACCESS_KEY'],
                                        aws_secret_access_key=os.environ['LOCAL_AWS_SECRET_KEY'],)
            verification_token = os.urandom(16).encode('hex');
            s3url = 'https://xyz.com/'
            verification_url = s3url+'?vtoken='+verification_token+'&uemail='+body['email'].strip()

            email_response = email_client.send_email(
                Source='akshay2626@gmail.com',
                Destination={
                    'ToAddresses': [
                        body['email'].strip(),
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
                            'Data': 'Use <a href="'+verification_url+'">this</a> url to verify.',
                            'Charset': 'UTF-8'
                        }
                    }
                },
                ReplyToAddresses=[
                    'akshay2626@gmail.com',
                ],
            )
        except ClientError as email_err:
            print email_err.response
            return error(500, 'Error sending email')
        # email config END

        return {
            'success': True,
            'message': 'Customer signup successful'
        }