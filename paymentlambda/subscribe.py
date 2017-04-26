"""
Handle Event Subscriptions
"""

class Queue:
    """
    Subscribed queue
    """
    WAIT_TIME_S = 3 #wait time in seconds for long polling
    MAX_MESSAGES = 10 #maximum number of messages
    PAYMENT_URL = 'https://sqs.us-east-1.amazonaws.com/908762746590/payment_queue'
