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
		else:
			self.send_vote_response(message, False)

	def handle_append_entries(self, message):
		self.refresh_timeout()
		if message.term<self.server.currentTerm:
			self.send_bad_response(message)

		if message.data is None:
			self.send_bad_response(message)
		elif message.data=={}:
			pass
		else:
			log=self.server.log
			data=message.data

			if "leaderCommit" not in data.keys() or "prevLogIndex" not in data.keys() or "prevLogTerm" not in data.keys():
				self.send_bad_response(message)
			else:
				if data["leaderCommit"]!=self.server.commitIndex:
					self.server.commitIndex=min(data["leaderCommit"], len(log)-1)

				if len(log)<data["prevLogIndex"]:
					self.send_append_entries_response(message, False)

				if len(log)>0 and lod[data["prevLogIndex"]]["term"]!=data["prevLogTerm"]:
					'''
						wait to implement
					'''
					pass


	def send_vote_response(self, message, voteGranted):
		data={"voteGranted": voteGranted}
		response=VoteResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	def send_append_entries_response(self, message, success):
		data={"success": success}
		response=AppendEntriesResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	def send_bad_response(self, message):
		data={}
		response=BadResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	def handle_message(self):
		if message.type is None or message.term is None:
			self.send_bad_response(message)
		m_type=message.type
		if message.term>self.server.currentTerm:
			self.server.currentTerm=term
		elif message.term<self.server.currentTerm:
			self.send_bad_response(message)

		if m_type==BaseMessage.APPEND_ENTRIES_REQUEST:
			self.handle_append_entries(message)
		elif m_type==BaseMessage.VOTE_REQUEST:
			self.handle_vote_request(message)
		elif m_type==BaseMessage.BAD_RESPONSE:
			print("ERROR! This message is bad. "+str(message))
		else:
			pass