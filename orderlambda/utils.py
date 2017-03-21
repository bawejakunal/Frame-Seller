import json
import os
import pymysql

def respond(resp, resp_code):
    return {
        'statusCode': resp_code,
        'body': json.dumps(resp),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

class Response:
    OK = '200'
    BAD = '400'
    FORBIDDEN = '403'
    INT_SER_ERR = '500'

def get_mysql_connection():
    rds_dbname = os.environ['dbname']
    rds_username = os.environ['dbusername']
    rds_password = os.environ['dbpassword']
    rds_host = os.environ['dbhost']
    rds_port = int(os.environ['dbport'])

    return pymysql.connect(host=rds_host, port=rds_port,
                            user=rds_username, passwd=rds_password,
                            db=rds_dbname, connect_timeout=5,
                            cursorclass=pymysql.cursors.DictCursor)

def get_order_query(userid, orderid=None):
    if orderid is None:
        return ("select id, product_id, product_url, user_id, paymentstatus,\
                orderdate from " + os.environ['tablename_order']
                + " where user_id = '" + userid + "'")
    else:
        return ("select id, product_id, user_id, product_url, paymentstatus, \
                orderdate from " + os.environ['tablename_order']
                + " where user_id = '" + userid + "' AND id = " + str(orderid))

def create_order_query():
    return ("INSERT INTO "+os.environ["tablename_order"]
        + " (`orderdate`, `token`, `paymentstatus`, `product_id`, `product_url`, `product_price`, `user_id`) VALUES \
        (%s, %s, %s, %s, %s, %s, %s)")





