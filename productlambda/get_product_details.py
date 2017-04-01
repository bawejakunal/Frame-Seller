from __future__ import print_function

import os
import pymysql
from responses import Response, respond
from hateoas import hateoas_constraints

"""
Getting MySQL connection
"""
def get_mysql_connection():
    # Reading from OS Environments for table
    rds_dbname = os.environ['dbname']
    rds_username = os.environ['dbusername']
    rds_password = os.environ['dbpassword']
    rds_host = os.environ['dbhost']
    rds_port = int(os.environ['dbport'])

    return pymysql.connect(host=rds_host, port=rds_port,
                           user=rds_username, passwd=rds_password,
                           db=rds_dbname, connect_timeout=5,
                           cursorclass=pymysql.cursors.DictCursor)

def get_json(prow, host, stage, path, mul_order):
    prow["links"] = hateoas_constraints(mul_order, host, stage, path,prow['id'])
    return prow

def get_product_query(pid=None):
    if pid is None:
        return ("select id, price, description, url from "+ os.environ['product_tablename'])
    else:
        return ("select id, price, description, url from " + os.environ['product_tablename'] + " where id = " + str(pid))

def get_product_details(event):
    response_json = {}
    err = False
    error_code = Response.INT_SER_ERR

    # Getting parameters
    path_parameters = event["pathParameters"]
    stage = event["requestContext"]["stage"]
    path = event["path"]
    host = event["headers"]["Host"]

    if path_parameters is None:
        # If no path parameters, return all orders
        product_list = []
        try:
            conn = get_mysql_connection()
        except:
            response_json = {"error": "System is facing some issues. Please try again later."}
            return respond(response_json, Response.INT_SER_ERR)

        try:
            with conn.cursor() as cur:
                cur.execute(get_product_query())

                for prow in cur:
                    prd = get_json(prow, host, stage, path, True)
                    product_list.append(prd)

            response_json["products"] = product_list
            response_json["links"] = hateoas_constraints(True, host, stage, path) # arg 1 unused
        except:
            err = True
            # Not setting error_code and using default
            response_json = {"error": "System is facing some issues. Please try again later."}
        finally:
            cur.close()
            conn.close()
            if err:
                return respond(response_json, error_code)
            else:
                return respond(response_json, Response.OK)

    elif path_parameters is not None and "productid" in path_parameters:
        # If there is pa in path parameters, return particular order having that orderid
        pid = path_parameters["productid"]
        
        # Check whether pid is a valid int or give error
        try:
            pid = int(pid)
        except ValueError:
            response_json = {"error": "Bad Request"}
            return respond(response_json, Response.BAD)

        try:
            conn = get_mysql_connection()
        except:
            response_json = {"error": "System is facing some issues. Please try again later."}
            return respond(response_json, Response.INT_SER_ERR)

        try:
            with conn.cursor() as cur:
                cur.execute(get_product_query(pid))

                if cur.rowcount == 0:
                    err = True
                    error_code = Response.FORBIDDEN
                    response_json = {"error": "No product found"}
                else:
                    for prow in cur:
                        response_json = get_json(prow, host, stage, path, False)
        except Exception as exp:
            print(exp.message)
            err = True
            # Not setting error_code and using default Response.INT_SER_ERR = '500'
            response_json = {"error": "System is facing some issues. Please try again later."}
        finally:
            cur.close()
            conn.close()
            if err:
                return respond(response_json, error_code)
            else:
                return respond(response_json, Response.OK)