"""
Handle Event Subscriptions
"""

#set of topics
Subscription = {
    'arn:aws:sns:us-east-1:908762746590:order-update': 'order-update'
}

class Queue:
    """
    Subscribed queue
    """
    WAIT_TIME_S = 3 #wait time in seconds for long polling
    MAX_MESSAGES = 10 #maximum number of messages
    ORDER_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/908762746590/Order-Queue'
