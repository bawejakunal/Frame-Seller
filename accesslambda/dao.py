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
    table = boto3.resource('dynamodb').Table('access-table')

    @classmethod
    def put_item(cls, item):
        """
        add item to user table
        """
        try:
            response = cls.table.put_item(Item=item)
        except ClientError as err:
            print(err)
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
