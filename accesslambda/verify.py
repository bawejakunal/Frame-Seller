"""
verify user access
"""

from dao import Dao, UnknownDbException

def verify_access(event):
    """
    verify access rule for user
    """
    uid = event['uid']
    resource = event['resource']

    try:
        key_dict = {
            'uid': uid,
            'resource': resource
        }
        print(key_dict)
        item = Dao.get_item(key_dict)

        if item is not None:
            return True

    except UnknownDbException as err:
        print(err)
    except Exception as err:
        print err
    return False
