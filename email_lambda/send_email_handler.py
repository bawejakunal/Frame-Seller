import boto3
import os
from botocore.exceptions import ClientError
import json
import urllib

def send_email_handler(event, context):
    # TODO implement
    print("Event")
    print(event)
    
    client = boto3.client('stepfunctions')
    
    response = client.get_activity_task(
        activityArn='arn:aws:states:us-east-1:908762746590:activity:sendEmailActivity',
        workerName='sendemaillambdaworker'
    )
    
    print(response["taskToken"])
    print(response["input"])
    print(type(response["input"]))
    
    taskToken = urllib.quote_plus(response["taskToken"],"")
    input_json = json.loads(response["input"])
    
    if input_json is None:
        print "None"
    else:
        print input_json
    
    """
    send verification email
    """
    if 'uemail' not in input_json or 'vtoken' not in input_json or 'verify_page' not in input_json:
        print('400:Bad Request')
    try:
        aws_access_key_id = os.environ['LOCAL_AWS_ACCESS_KEY']
        aws_secret_access_key = os.environ['LOCAL_AWS_SECRET_KEY']
        email_client = boto3.client('ses', aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key
                                   )
        s3url = input_json['verify_page'].strip().strip('/')
        
        succeed_verification_url = (s3url + '?vtoken=' + input_json['vtoken'] + '&uemail='+input_json['uemail'] +'&taskToken='+taskToken + '&verify=succeed')
        fail_verification_url = (s3url + '?vtoken=' + input_json['vtoken'] + '&uemail='+input_json['uemail'] +'&taskToken='+taskToken + '&verify=succeed')
                           
        response = email_client.send_email(
            Source='akshay2626@gmail.com',
            Destination={
                'ToAddresses': [
                    input_json['uemail'],
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
                        'Data': 'Use this url to verify:'+succeed_verification_url+'. If you didn\'t register,click url:'+fail_verification_url,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': 'Use <a href="'+succeed_verification_url+'">this url </a>to verify.If you didn\'t register,click on this <a href="'+fail_verification_url+'">url</a>',
                        'Charset': 'UTF-8'
                    }
                }
            },
            ReplyToAddresses=[
                'akshay2626@gmail.com',
            ],
        )
        print('Email inserted to send queue')
        return {
            'success': True,
            'message': 'Email inserted to send queue'
        }
    except ClientError as email_err:
        print('500:Error sending email')
    
    # email config END