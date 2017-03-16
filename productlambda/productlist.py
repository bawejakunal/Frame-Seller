from __future__ import print_function

import boto3
import json

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

try:
    rds_dbname = os.environ['stripedemo']
    rds_username = os.environ['dbusername']
    rds_password = os.environ['dbpassword']
    rds_host = os.environ['dbhostname'] + ":" + os.environ['dbport']
    conn = pymysql.connect(rds_host, user=rds_username, passwd=rds_password, db=rds_dbname, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()


def product_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    
    #print("Received event: " + json.dumps(event, indent=2))
    item_count = 0

    with conn.cursor() as cur:
        cur.execute("select * from "+ os.environ['product_tablename'])
        for row in cur:
            print row
            item_count += 1
    

    
    
    return "Hello " +str(item_count)