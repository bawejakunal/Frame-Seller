from __future__ import print_function

import boto3
from error import error
from botocore.exceptions import ClientError

def verify_customer(body):
    if ('uemail' not in body) or\
        ('vtoken' not in body):
        return error(401, 'email or token not found')

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
        customer_info = None
        if 'Item' not in response:
            return error(404, 'Customer does not exist')
        # user retrieved from database
        _item = response['Item']
        _verification = _item['verification']
        if _verification['token'] == body['vtoken']:
            verifiction_response = {
                'success': True,
                'message': 'Congrats! Your email has been verified successfully.'
            }
            return verifiction_response
        else:
            return error(401, 'Email verification failed!')
