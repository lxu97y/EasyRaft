import shlex, subprocess
import unittest
import time
import sys
sys.path.append("..")
from src.message.message import *
from src.client.client import Client

class Test(unittest.TestCase):
	def test_get(self):
		client=Client()
		client.put('a',1)
		client.put('b',2)
		client.put('c',3)
		client.get('a')
		client.get('b')
		client.get('c')
		
	def test_put(self):
		client=Client()
		client.put('a',1)
		client.put('b',2)
		client.put('c',3)
		client.put('a',1)
		client.put('b',2)
		client.put('c',3)

if __name__ == '__main__':
	cl="python test_election_one_candidate.py"
	args = shlex.split(cl)
	process = subprocess.Popen(args)
	#wait for nodes initialization
	time.sleep(1)
	unittest.main()
	time.sleep(1)
	process.terminate()