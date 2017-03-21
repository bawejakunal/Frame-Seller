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
    table = boto3.resource('dynamodb').Table('Customer')

    @classmethod
    def put_item(cls, item):
        """
        add item to user table
        """
        try:
            response = cls.table.put_item(Item=item,
                ConditionExpression="attribute_not_exists(uid) AND attribute_not_exists(email)")
        except ClientError as err:
            if (err.response['Error']['Code'] ==
                'ConditionalCheckFailedException'):
                raise AlreadyExistException('User Already Exists')
            else:
                raise UnknownDbException('Unknown error creating entry')

    @classmethod
    def get_item(cls, key, value):
        """
        get item from database by key
        return None if no matching item found
        """
        try:
            response = cls.table.get_item(Key={key: value})

            #no result with matching key
            if 'Item' not in response:
                return None

            item = response['Item']
            return item

        except ClientError as err:
            print(err)
            raise UnknownDbException('Unable to fetch item')

    @classmethod
    def update_item(cls, key, keyval, attr, value):
        try:
            response = cls.table.update_item(
                Key={key: keyval},
                UpdateExpression="set %s = :x" % attr,
                ExpressionAttributeValues={':x':value},
                ReturnValues="UPDATED_NEW")
            return response
        except ClientError as err:
            print(err)
            raise UnknownDbException('Unable to update database')
