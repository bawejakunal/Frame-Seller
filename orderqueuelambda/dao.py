"""
Data abstraction class
"""

import boto3
from botocore.exceptions import ClientError

class AlreadyExistException(Exception):
    """
    Entry already exists in database
    """
    pass

class UnknownDbException(Exception):
    """
    Entry already exists in database
    """
    pass


class Dao(object):
    """
    access user table from here
    """
    table = boto3.resource('dynamodb').Table('OrderQueueDB')

    @classmethod
    def put_item(cls, item):
        """
        add item to user table
        """
        try:
            cls.table.put_item(Item=item,
                ConditionExpression="attribute_not_exists(order_id)") 
        except ClientError as err:
            print(err)
            if (err.response['Error']['Code'] ==
                'ConditionalCheckFailedException'):
                raise AlreadyExistException('Order Already Exists')
            else:
                raise UnknownDbException('Unknown error creating entry')

    @classmethod
    def get_item(cls, key_dict):
        """
        get item from database by key
        return None if no matching item found
        """
        try:
            response = cls.table.get_item(Key=key_dict)

            #no result with matching key
            if 'Item' not in response:
                return None

            item = response['Item']
            return item
        except ClientError as err:
            print(err)
            raise UnknownDbException('Unable to fetch item')

    @classmethod
    def update_item(cls, item):
        """
        completely overwrite the previous item
        """
        try:
            response = cls.table.put_item(Item=item, ReturnValues='ALL_OLD')
            return response
        except ClientError as err:
            print(err)
            raise UnknownDbException('Unable to update database')
