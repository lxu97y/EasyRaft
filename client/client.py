import zmq
from ..config import Config
from ..message.message import *

context=zmq.Context()
socket=context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:"%Config.CLIENT_PORT)
request=ServerRequest("GET", {"key": "a", "value": "1"})
socket.send_pyobj(request)
response=socket.recv_pyobj()
print(response)