import socket
import json

kv_store=dict()

def task(json_package, accepted_socket):
	response=parse(json_package)
	response_str=str(response)
	accepted_socket.send(response.encode('utf8'))
	accepted_socket.close()

def parse(json_package):
	action=json.loads(json_package)
	action_type=action['type']
	payload=action['payload']
	response=None
	if action_type=='put':
		response=put(payload)
	elif action_type=='get':
		response=get(payload)
	else:
		response=undefinedAction()
	return response

def put(payload):
	key=payload['key']
	value=payload['value']
	kv_store[key]=value
	response={'code':'success'}
	return json.dumps(response)

def undefinedAction():
	response={'code':'undefined action'}
	return json.dumps(response)