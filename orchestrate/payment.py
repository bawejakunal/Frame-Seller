"""
Payment processing module
"""

class Status(object):
    """
    Describe payment status
    """
    UNPAID = 0
    PAID = 1
    FAILED = 2
