import unittest
import sys
import socket
import json
class Test(unittest.TestCase):
   
    def test_put(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(('localhost',6000))
        data = {
            'type':'put',
            'payload':{
                'key':'a',
                'value':'a',
                }
            }
        server_socket.send(json.dumps(data).encode('utf-8'))
        recv_data = server_socket.recv(1024)
        js = json.loads(recv_data.decode())
        self.assertTrue(js['code']=='success')

if __name__ == '__main__':
    unittest.main()
