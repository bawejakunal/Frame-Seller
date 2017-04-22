"""
Order queue handling lambda
"""

from __future__ import print_function

import urlparse
from orderdb import add_order
from error import error

def handler(event, context):
    #signup or login operation
    try:
        print(event)
        if 'operation' not in event or 'body-json' not in event:
            return error(400, 'Invalid operation')

        operation = event['operation']
        body = event['body-json']

        if operation == 'update':
            pass

        elif operation == 'orderqueue':
            item = add_order(body)
            url = body['base-url']
            url = urlparse.urljoin(url, item['oid'])
            return {
                'status': 'Accepted',
                'Location': url
            }

        else:
            return error(400, 'Invalid operation')

    except KeyError as err:
        print(err)
        return error(400, 'Invalid operation')
