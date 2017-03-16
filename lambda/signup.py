"""
User module to signup user
"""

import boto3
from botocore.exceptions import ClientError
from error import error

def create_customer(event):
    """
    Create customer entry in table
    """

    #validate required entries
    if ('firstname' not in event) or\
        ('lastname' not in event) or\
        ('email' not in event) or\
        ('password' not in event):
        return error(400, 'Missing parameters')

    #get the Customer table
    user_table = boto3.resource('dynamodb').Table('Customer')
    
    try:
        response = user_table.put_item(
            Item={
                'email' : event['email'].strip(), #primary key in 
                'info' : {
                    'first' : event['firstname'].strip(),
                    'last' : event['lastname'].strip(),
                    'password' : event['password'].strip(), #TODO: hash, salt
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
