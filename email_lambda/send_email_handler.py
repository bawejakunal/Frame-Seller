from __future__ import print_function
import os
import boto3
from botocore.exceptions import ClientError

def send_email_handler(event, context):
    """
    send verification email
    """
    if 'uemail' not in event or 'vtoken' not in event:
        return error(400,'Bad request')
    try:
        aws_access_key_id = os.environ['LOCAL_AWS_ACCESS_KEY']
        aws_secret_access_key = os.environ['LOCAL_AWS_SECRET_KEY']
        email_client = boto3.client('ses', aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key
                                   )
        s3url = 'https://xyz.com/'
        
        verification_url = (s3url + '?vtoken=' + event['vtoken'] +
                           '&uemail='+event['uemail'])
                           
        response = email_client.send_email(
            Source='akshay2626@gmail.com',
            Destination={
                'ToAddresses': [
                    event['uemail'],
                ],
                'BccAddresses': [
                ],
                'CcAddresses': [
                ],
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
            ReplyToAddresses=[
                'akshay2626@gmail.com',
            ],
        )
        return {
            'success': True,
            'message': 'Email inserted to send queue'
        }
    except ClientError as email_err:
        print(email_err.response)
        return error(500, 'Error sending email')
    
    # email config END