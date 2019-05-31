import zmq
from ..config import Config
from ..message.message import *

id=1
ip=Config.NODE_LIST[str(id)][0]
port=Config.NODE_LIST[str(id)][2]

def init_socket(ip, port):
	context=zmq.Context()
	socket=context.socket(zmq.REQ)
	socket.connect("tcp://"+ip+":"+port)
	return socket

def put(socket, key, value):
	request=ServerRequest("PUT", {"key": "a", "value": "1"})
	socket.send_pyobj(request)
	response=socket.recv_pyobj()
	if response.code=='300':
		data=response.data
		socket=init_socket(data["ip_address"], data["port"])
		response=socket.recv_pyobj()
		if response.code=='200':
			print("put value successfully.")
		elif response.code=='400':
			print("fail.")
	elif response.code=='200':
		print("put value successfully.")
	elif response.code=='400':
		print("fail.")
	elif response.code=='500':
		print("Server failed.")

def get(socket, key):
	request=ServerRequest("GET", {"key": "a"})
	socket.send_pyobj(request)
	response=socket.recv_pyobj()
	if response.code=='300':
		data=response.data
		socket=init_socket(data["ip_address"], data["port"])
		response=socket.recv_pyobj()
		if response.code=='200':
			value=response.data['value']
			print(value)
		elif response.code=='400':
			print("400, no value.")
		else:
			print("Server failed.")
	elif response.code=='200':
		value=response.data['value']
		print(value)
	elif response.code=='400':
		print("400, no value.")
	elif response.code=='500':
		print("Server failed.")
	return value