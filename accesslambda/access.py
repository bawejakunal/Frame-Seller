"""
maintain access rules for custom authorizer
"""

from queue import update_database
from verify import verify_access

SCHEDULE_ARN = 'arn:aws:events:us-east-1:908762746590:rule/AccessRuleSchedule'

def handler(event, context):
    """
    this handler is invoked in two ways
    """
    if 'resources' in event and SCHEDULE_ARN in event['resources']:
        update_database(event)

    elif 'operation' in event and event['operation'] == 'verify':
        return verify_access(event)
