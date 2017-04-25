"""
maintain access rules for custom authorizer
"""

from queue import update_database

SCHEDULE_ARN = 'arn:aws:events:us-east-1:908762746590:rule/AccessRuleSchedule'

def handler(event, context):
    """
    this handler is invoked in two ways
    """
    if 'resources' in event and SCHEDULE_ARN in event['resources']:
        update_database(event)
    