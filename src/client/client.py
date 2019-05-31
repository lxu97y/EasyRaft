import zmq
from ..config import Config
from ..message.message import *

ip=Config.NODE_LIST['1'][0]
port=Config.NODE_LIST['1'][2]
context=zmq.Context()
socket=context.socket(zmq.REQ)
socket.connect("tcp://"+ip+":"+port)
request=ServerRequest("GET", {"key": "a", "value": "1"})
socket.send_pyobj(request)
response=socket.recv_pyobj()
if response.code=='300':
	data=response.data
	socket=context.socket(zmq.REQ)
	socket.connect("tcp://"+data["ip_address"]+":"+data["port"])
	socket.send_pyobj(request)
	response=socket.recv_pyobj()
	print(response)
elif:
	print("Server failed.")