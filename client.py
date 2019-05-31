import zmq
from src.config import Config
from src.message.message import *
from random import randint

context=zmq.Context()
socket=context.socket(zmq.REQ)
#str(randint(1,Config.NUMBER_TOTAL_NODES)) 
socket.connect("tcp://127.0.0.1:%s"%Config.NODE_LIST['1'][2])
request=ServerRequest("PUT", {"key": "a", "value": "1"})
socket.send_pyobj(request)
print("send success")
response=socket.recv_pyobj()
print(response.code)
