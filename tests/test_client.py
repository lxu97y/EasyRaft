import shlex, subprocess
import unittest
import time
import random
import sys
sys.path.append("..")
from src.message.message import *
from src.client.client import Client

class Test(unittest.TestCase):
	def test_get(self):
		print("GET test.")
		client=Client()
		for i in range(0,100):
			key=random.randint(0,10000)
			value=random.randint(0,10000)
			client.put(key, value)
			return_value=client.get(key)
			self.assertTrue(value==return_value)
		print()
		
	def test_put(self):
		print("PUT test.")
		client=Client()
		for i in range(0,100):
			client.put(random.randint(0,10000), random.randint(0,10000))
		print()

if __name__ == '__main__':
	cl="python test_election_one_candidate.py"
	args = shlex.split(cl)
	process = subprocess.Popen(args)
	#wait for nodes initialization
	time.sleep(1)
	unittest.main()
	time.sleep(1)
	process.terminate()