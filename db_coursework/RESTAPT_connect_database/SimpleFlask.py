# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy



import WebBO
# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():

	fields = None
	in_args = None
	if request.args is not None:
		print(request.args)
		in_args = dict(copy.copy(request.args))
		fields = copy.copy(in_args.get('fields', None))
		offset = copy.copy(in_args.get('offset', None))
		limit = copy.copy(in_args.get('limit', None))
		if fields:
			del(in_args['fields'])
		if offset:
			del(in_args['offset'])
		if limit:
			del(in_args['limit'])

	try:
		if request.data:
			body = json.loads(request.data)
		else:
			body = None
	except Exception as e:
		print("Got exception = ", e)
		body = None


	print("Request.args : ", json.dumps(in_args))
	return in_args, fields, offset, limit, body




@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):

	in_args, fields, offset, limit, body = parse_and_print_args()
	current_url = request.url
	next_url, offset, limit = WebBO.generate_next_url(current_url, offset, limit)

	if request.method == 'GET':
		try:
			result = WebBO.find_by_template(resource, \
											   in_args, fields, offset, limit)
			result = {"data": result, "link": [{"current": current_url}, {"next": next_url}]}
			if result:
				return json.dumps(result, indent=2), 200, \
				   {"content-type": "application/json; charset: utf-8"}
			else:
				return "Not Found ", 404
		except Exception as e:
			return "Method " + request.method + " on resource " + resource + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}


	elif request.method == 'POST':
		print("on table ", resource)
		print("with row ", body)
		
		try:
			WebBO.insert(resource, body)
			return "Method " + request.method + " on resource " + resource + \
				" successfully implemented!", 501, {"content-type": "text/plain; charset: utf-8"}
		except Exception as e:
			return "Method " + request.method + " on resource " + resource + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}

	else:
		return "Method " + request.method + " on resource " + resource + \
			   " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>', methods=['GET', 'PUT', 'DELETE'])
def get_resource_key(resource, primary_key):
	in_args, fields, offset, limit, body = parse_and_print_args()
	current_url = request.url
	next_url, offset, limit = WebBO.generate_next_url(current_url, offset, limit)

	primary_key = primary_key.split('_')
	if request.method == 'GET':
		try:
			result = WebBO.find_by_primary_key(resource, primary_key, fields, offset, limit)
			result = {"data": result, "link": [{"current": current_url}, {"next": next_url}]}

			if result:
				return json.dumps(result, indent=2), 200, \
					{"content-type": "application/json; charset: utf-8"}
			else: 
				return "Not Found ", 404 
		except Exception as e:
			return "Method " + request.method + " on resource " + resource + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}

	elif request.method == 'PUT':
		print("on table", resource)
		print('with row', body)

		try:
			WebBO.update_given_primary_key(resource, body, primary_key)
			return "Method " + request.method + " on resource " + resource + \
				" successfully implemented!", 501, {"content-type": "text/plain; charset: utf-8"}
		except Exception as e:
			return "Method " + request.method + " on resource " + resource + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}

	elif request.method == 'DELETE':
		try:
			WebBO.delete_given_primary_key(resource, primary_key)
			return "Method " + request.method + " on resource " + resource + \
				" successfully implemented!", 501, {"content-type": "text/plain; charset: utf-8"}
		except Exception as e:
			return "Method " + request.method + " on resource " + resource + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}


	else:
		return "Method " + request.method + " on resource " + resource + \
			   " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=['GET', 'POST'])
def get_dependent_resource(resource, primary_key, related_resource):
	in_args, fields, offset, limit, body = parse_and_print_args()

	current_url = request.url
	next_url, offset, limt = WebBO.generate_next_url(current_url, offset, limit)

	primary_key = primary_key.split('_')
	print(primary_key)
	if request.method == 'GET':
		try: 
			result = WebBO.generate_dependent_result(resource, primary_key, related_resource, fields, offset, limit)
			result = {"data": result, "link": [{"current": current_url}, {"next": next_url}]}

			if result:
				return json.dumps(result, indent=2), 200, \
					{"content-type": "application/json; charset: utf-8"}
			else: 
				return "Not Found ", 404
		except Exception as e:
			return "Method " + request.method + " on resource " + resource + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}

	elif request.method == 'POST':
		print("on table ", related_resource)
		print("with row ", body)
		
		try:
			WebBO.insert_dependent(resource, primary_key, related_resource, body)
			return "Method " + request.method + " on resource " + resource + \
				" successfully implemented!", 501, {"content-type": "text/plain; charset: utf-8"}		
		except Exception as e:
			return "Method " + request.method + " on resource " + resource + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}

	else:
		return "Method " + request.method + " on resource " + resource + \
			   " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/teammates/<playerid>', methods=['GET'])
def get_teammate(playerid):
	in_args, fields, offset, limit, body = parse_and_print_args()

	current_url = request.url
	next_url, offset, limit = WebBO.generate_next_url(current_url, offset, limit)

	if request.method == 'GET':
		try: 
			result = WebBO.generate_teammate(playerid, offset, limit)
			result = {"data": result, "link": [{"current": current_url}, {"next": next_url}]}

			if result:
				return json.dumps(result, indent=2), 200, \
					{"content-type": "application/json; charset: utf-8"}
			else: 
				return "Not Found ", 404
		except Exception as e:
			return "Method " + request.method + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}	
	else:
		return "Method " + request.method + \
			   " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/people/<playerid>', methods=['GET'])
def get_career_stats(playerid):
	in_args, fields, offset, limit, body = parse_and_print_args()

	current_url = request.url
	next_url, offset, limit = WebBO.generate_next_url(current_url, offset, limit)

	if request.method == 'GET':
		try: 
			print(next_url)
			result = WebBO.generate_career_stats(playerid, offset, limit)
			result = {"data": result, "link": [{"current": current_url}, {"next": next_url}]}

			if result:
				return json.dumps(result, indent=2), 200, \
					{"content-type": "application/json; charset: utf-8"}
			else: 
				return "Not Found ", 404
		except Exception as e:
			return "Method " + request.method + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}	
	else:
		return "Method " + request.method + \
			   " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/roster', methods=['GET'])
def get_roster():
	in_args, fields, offset, limit, body = parse_and_print_args()
	teamid = in_args["teamid"][0]
	yearid = in_args["yearid"][0]


	current_url = request.url
	next_url, offset, limit = WebBO.generate_next_url(current_url, offset, limit)

	if request.method == 'GET':
		try: 
			print(next_url)
			result = WebBO.generate_roster(teamid, yearid, offset, limit)
			result = {"data": result, "link": [{"current": current_url}, {"next": next_url}]}

			if result:
				return json.dumps(result, indent=2), 200, \
					{"content-type": "application/json; charset: utf-8"}
			else: 
				return "Not Found ", 404
		except Exception as e:
			return "Method " + request.method + " internal error: " + \
				str(e), 501, {"content-type": "text/plain; charset: utf-8"}	
	else:
		return "Method " + request.method + \
			   " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}	

if __name__ == '__main__':
	app.run()

