"""
User module to signup user
"""
import os
import uuid
import boto3
from botocore.exceptions import ClientError
from error import error
from verify import send_email

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

    verification_token = os.urandom(16).encode('hex')

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
                    'verified' : False
                },
                'verification':{
                    'token' : verification_token
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
        email = body['email'].strip()
        send_email(email, verification_token)

        return {
            'success': True,
            'message': 'Customer signup successful'
        }
