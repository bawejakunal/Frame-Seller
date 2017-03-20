from __future__ import print_function

import os
import pymysql
from responses import Response, respond

def post_order(event):
	print(event["body"])
	return respond(event, Response.OK)
