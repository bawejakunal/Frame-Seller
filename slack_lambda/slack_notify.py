'''
Follow these steps to configure the webhook in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Incoming WebHooks".

  3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".

  4. Copy the webhook URL from the setup instructions and use it in the next section.

To encrypt your secrets use the following steps:

  1. Create or use an existing KMS Key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html

  2. Click the "Enable Encryption Helpers" checkbox

  3. Paste <SLACK_HOOK_URL> into the kmsEncryptedHookUrl environment variable and click encrypt

  Note: You must exclude the protocol from the URL (e.g. "hooks.slack.com/services/abc123").

  4. Give your function's role permission for the kms:Decrypt action.

     Example:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1443036478000",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "<your KMS key ARN>"
            ]
        }
    ]
}
'''
from __future__ import print_function

import boto3
import json
import logging
import os

from base64 import b64decode
from urllib2 import Request, urlopen, URLError, HTTPError

from subscribe import Subscription

# The base-64 encoded, encrypted key (CiphertextBlob) stored in the kmsEncryptedHookUrl environment variable
ENCRYPTED_HOOK_URL = os.environ['kmsEncryptedHookUrl']

# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ['slackChannel']

HOOK_URL = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext']

# initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def slack_handler(event, context):
    """
    handle slack notifications from sns
    """

    if 'Records' in event:
        sns = event['Records'][0]['Sns']
        topic_arn = sns['TopicArn']
        message = json.loads(sns['Message'])

        #slack hook POST request HTTP headers
        headers = {'Content-type': 'application/json'}

        #send customer create notification
        if Subscription[topic_arn] == 'customer-create':
            # create customer create notification message
            uid = message['uid']
            email = message['email']
            slack_message = {
                'channel': SLACK_CHANNEL,
                'text': "%s registered with user id %s" % (email, uid)
            }

            # create and open request to slack webhook url
            req = Request(HOOK_URL, json.dumps(slack_message), headers)
            try:
                response = urlopen(req)
                response.read()
            except HTTPError as err:
                logger.error("Request failed: %d %s", err.code, err.reason)
            except URLError as err:
                logger.error("Server connection failed: %s", err.reason)
