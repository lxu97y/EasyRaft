import zmq
from ..config import Config
from ..message.message import *

class Client(object):
	def __init__(self):
		#default
		self.id=1
		self.ip=Config.NODE_LIST[str(self.id)][0]
		self.port=Config.NODE_LIST[str(self.id)][2]

	def init_socket(self):
		context=zmq.Context()
		socket=context.socket(zmq.REQ)
		socket.connect("tcp://"+self.ip+":"+str(self.port))
		return socket

	def put(self, key, value):
		socket=self.init_socket()
		request=ServerRequest("PUT", {"key": key, "value": value})
		socket.send_pyobj(request)
		try:
			response=socket.recv_pyobj()
			if response.code=='300':
				data=response.data
				self.ip=response.data["ip_address"]
				self.data=response.data["port"]
				socket=self.init_socket()
				response=socket.recv_pyobj()
				if response.code=='200':
					print("put (%s,%s) successfully."%(str(key),str(value)))
				elif response.code=='400':
					print("put fails.")
			elif response.code=='200':
				print("put (%s,%s) successfully."%(str(key),str(value)))
			elif response.code=='400':
				print("put fails.")
			elif response.code=='500':
				print("Server failed.")
		except Exception as e:
			print(e)
		socket.close()

	def get(self, key):
		value=None
		socket=self.init_socket()
		request=ServerRequest("GET", {"key": key})
		socket.send_pyobj(request)
		try:
			response=socket.recv_pyobj()
			if response.code=='300':
				data=response.data
				self.ip=response.data["ip_address"]
				self.data=response.data["port"]
				socket=self.init_socket()
				response=socket.recv_pyobj()
				if response.code=='200':
					value=response.data['value']
					print("get successfully: (%s,%s)"%(str(key),str(value)))
				elif response.code=='400':
					print("get fails. no value.")
				else:
					print("Server failed.")
			elif response.code=='200':
				value=response.data['value']
				print("get successfully: (%s,%s)"%(str(key),str(value)))
			elif response.code=='400':
				print("get fails. no value.")
			elif response.code=='500':
				print("Server failed.")
		except Exception as e:
			print(e)
		socket.close()
		return value