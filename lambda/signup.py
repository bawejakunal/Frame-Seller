"""
User module to signup user
"""

import boto3
from botocore.exceptions import ClientError
from error import error

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
                'email' : body['email'].strip(), #primary key in 
                'info' : {
                    'firstname' : body['firstname'].strip(),
                    'lastname' : body['lastname'].strip(),
                    'password' : body['password'].strip(), #TODO: hash, salt
                    'active': True,
                    'verified' : True #TODO: email verification
                }
            },
            ConditionExpression="attribute_not_exists(email)"
        )

    except ClientError as err:
        if err.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return error(400, 'User already exists')
        else:
            print(err)
        return error(500, 'Error creating user entry')

    else:
        return {
            'success': True,
            'message': 'Customer signup successful'
        }
