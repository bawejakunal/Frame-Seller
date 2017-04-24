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

    @classmethod
    def query(cls, query_dict):
        """
        get all items defined by key dictionary
        """
        try:
            condition_list = list()
            expression_attr_values = dict()
            for key in query_dict:
                condition_list.append('%s = :%s' % (key, key))
                expression_attr_values[":" + str(key)] = query_dict[key]
            key_condition_expression = " AND ".join(condition_list)

            response = cls.table.query(Select='ALL_ATTRIBUTES',
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attr_values,
                FilterExpression='attribute_not_exists(redirect_url)')

            print(response)
            return response['Items']

        except ClientError as err:
            print(err)
            raise UnknownDbException('Unable to query database')
