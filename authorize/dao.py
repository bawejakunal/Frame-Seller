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


class DoesNotExistException(Exception):
    """
    Entry not found in database
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
    def get_item(cls):
        pass
