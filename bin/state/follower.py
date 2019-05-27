import time
import random
from ..message.message import *
from ..state.state import State
from ..config import Config

class Follower(State):
	def __init__(self,server=None):
		State.__init__(self, server)
		if self.server:
			self.server.refresh_election_timer()

	def send_append_entries_response(self, message, success):
		data={"success": success}
		response=AppendEntriesResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	def handle_append_entries_request(self, message):
		# self.refresh_election_timeout()
		# if message.term<self.server.currentTerm:
		# 	self.send_append_entries_response(message, False)
		# 	return

		# if message.data is None or message.data={}:
		# 	self.send_append_entries_response(message, False)
		# 	return
		# else:
		# 	log=self.server.log
		# 	data=message.data

		# 	if "leaderCommit" not in data.keys() or "prevLogIndex" not in data.keys() or "prevLogTerm" not in data.keys():
		# 		self.send_append_entries_response(message, False)
		# 		return
		# 	else:
		# 		# index is from 1, so here is <=
		# 		if len(log)<=data["prevLogIndex"]:
		# 			self.send_append_entries_response(message, False)
		# 			return

		# 		if len(log)>0 and log[data["prevLogIndex"]]["term"]!=data["prevLogTerm"]:
		# 			#delete the existing entry and all that follow it
		# 			self.server.log=log[0:data["prevLogIndex"]]
		# 			self.send_append_entries_response(message, False)
		# 			return
		# 		else:
		# 			#keep entries from 0 to prevLogIndex
		# 			log=log[0:data["prevLogIndex"]+1]
		# 			for x in data["entries"]:
		# 				log.append(x)
		# 				self.server.commitIndex=self.server.commitIndex+1
		# 			self.server.log=log
		# 			if data["leaderCommit"]>self.server.commitIndex:
		# 				self.server.commitIndex=min(data["leaderCommit"], self.server.lastLogIndex())
		# 			self.send_append_entries_response(message, True)
		pass