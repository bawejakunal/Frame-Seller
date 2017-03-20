"""
Lamdba Orchestrator
"""

from __future__ import print_function
import json
import boto3
import orders

def handler(event, context):
    """
    delegate work
    """
    print(event)
    if event['resource'].startswith('/orders'):
        return orders.order(event, context)
