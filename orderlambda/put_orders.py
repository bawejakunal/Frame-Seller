from __future__ import print_function

from utils import Response, respond, get_mysql_connection, get_update_query

def put_order_details(event):
	response_json = {}
	err = False
	error_code = Response.INT_SER_ERR

	data = event["data"]
	if "orderid" not in data or "paymentstatus" not in data:
		response_json = { "message" : "Bad Request" }
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
			cursor.execute(query)
			response_json = { "message" : "Orders updated" }
		except Exception as error:
			print(error)
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

