"""
send verification email
"""

import os
import boto3
from botocore.exceptions import ClientError

#no return expected
def verification_mail(customer_data):
    """
    send verification email
    """

    #drop request if malformed
    if ('email' not in customer_data) or ('verify_page' not in customer_data)\
        or ('verification' not in customer_data):
        return

    #extract details and send email
    event = {
        'uemail': customer_data['email'],
        'vtoken': customer_data['verification']['token'],
        'verify_page': customer_data['verify_page']
    }

    try:
        aws_access_key_id = os.environ['LOCAL_AWS_ACCESS_KEY']
        aws_secret_access_key = os.environ['LOCAL_AWS_SECRET_KEY']
        email_client = boto3.client('ses', aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key
                                   )
        s3url = event['verify_page'].strip().strip('/')
        
        verification_url = (s3url + '?vtoken=' + event['vtoken'] + '&uemail='+event['uemail'])
                           
        response = email_client.send_email(
            Source='akshay2626@gmail.com',
            Destination={
                'ToAddresses': [event['uemail'],],
                'BccAddresses': [],
                'CcAddresses': [],
            },
            Message={
                'Subject': {
                    'Data': 'Frameseller Email Verification',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'Use this url to verify:'+verification_url,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': 'Use <a href="'+verification_url+'">this url </a>to verify.',
                        'Charset': 'UTF-8'
                    }
                }
            },
            ReplyToAddresses=['akshay2626@gmail.com',]
        )
        print('Email inserted to send queue')
    except ClientError as err:
        print('ERROR: %s' % err)
