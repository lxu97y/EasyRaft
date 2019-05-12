import unittest
import sys

class Test(unittest.TestCase):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def test_put_get_normal():
        socket.create_connection(('localhost','5000'))
        data = {
            'type':'put',
            'payload':{
                'key':'a',
                'value':'a',
                }
            }
        socket.send()
        socket.recv

if __name__ == '__main__':
    unittest.main()
