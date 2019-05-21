import time
import random
from ..message.message import *

class Follwer(object):
	def __init__(self):
		self.timeout=random.randrange(150,300)
		self.server=None
		self.last_vote=None

	def set_server(self, server):
		self.server=server

	def refresh_timeout(self):
		self.timeout=random.randrange(150,300)

	def handle_vote_request(self, message):
		if "lastLogIndex" not in message.data.keys():
			self.send_vote_response(message, False)
		if self.last_vote is None and message.data["lastLogIndex"]>=self.server.lastLogIndex:
			self.last_vote=message.sender
			self.send_vote_response(message, True)
		else
			self.send_vote_response(message, False)

	def handle_append_entries(self, message):
		self.refresh_timeout()
		if message.term<self.server.currentTerm:
			self.send_append_entries_response(message, False)

		if message.data is None or message.data=={}:
			self.send_append_entries_response(message, False)
		else:


	def send_vote_response(self, message, voteGranted):
		data={"voteGranted": voteGranted}
		response=VoteResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	def send_append_entries_response(self, message, success):
		data={"success": success}
		response=AppendEntriesResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	def handle_message(self):

	