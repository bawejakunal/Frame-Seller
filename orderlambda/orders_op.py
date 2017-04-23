from __future__ import print_function

from utils import Response, respond, get_mysql_connection, get_update_query

from validator import validate_json_updatepayment

def update_order(payload):

    if not validate_json_updatepayment(payload):
        return [False, 'Invalid JSON']

	#Process the updation of the order
	return [True,""]



def put_order_details(data):
	response_json = {}
	err = False
	error_code = Response.INT_SER_ERR
	
	# Return Bad Request if orderid and paymentstatus is not in data
	if "orderid" not in data or "paymentstatus" not in data:
		response_json = { "message" : "Bad Request" }
		print(response_json)
		return respond(response_json, Response.BAD)
	else:
		orderid = data["orderid"]
		paymentstatus = data["paymentstatus"]

		try:
			conn = get_mysql_connection()
		except Exception as error:
			print(error)
			response_json = { "message" : "System is facing some issues" }
			return respond(response_json, Response.INT_SER_ERR)

		try:
			cur = conn.cursor()
			query = get_update_query(orderid, paymentstatus)
			rowcount = cur.execute(query)
			cur.connection.commit()
			# If query execution reaches here, create normal response
			response_json = { "message" : "Orders updated" }
		except Exception as error:
			err = True
			# using default error code
			response_json = { "message" : "Payment update failed" }
		finally:
			cur.close()
			conn.close()
			if err:
				respond(response_json, error_code)
			else:
				respond(response_json, Response.OK)

