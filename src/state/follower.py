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

	def send_append_entries_response(self, message, success, matchIndex):
		data={"success": success}
		if success==True:
			data["matchIndex"]=matchIndex
		response=AppendEntriesResponse(self.server.id, message.sender, message.term, data)
		self.server.publish_message(response)

	def handle_append_entries_request(self, message):
		self.server.refresh_election_timer()
		if message.term<self.server.currentTerm:
			self.send_append_entries_response(message, False, self.server.lastLogIndex())
			return

		if message.data is None or message.data=={}:
			self.send_append_entries_response(message, False, self.server.lastLogIndex())
			return
		else:
			log=self.server.log
			data=message.data

			if "leaderCommit" not in data.keys() or "prevLogIndex" not in data.keys() or "prevLogTerm" not in data.keys():
				self.send_append_entries_response(message, False, self.server.lastLogIndex())
				return
			else:
				# index is from 1, so here is <=
				if len(log)<=data["prevLogIndex"]:
					self.send_append_entries_response(message, False, self.server.lastLogIndex())
					return

				if len(log)>0 and log[data["prevLogIndex"]]["term"]!=data["prevLogTerm"]:
					#delete the existing entry and all that follow it
					self.server.log=log[0:data["prevLogIndex"]]
					self.send_append_entries_response(message, False, self.server.lastLogIndex())
					return
				else:
					#keep entries from 0 to prevLogIndex
					log=log[0:data["prevLogIndex"]+1]
					for x in data["entries"]:
						log.append(x)
						self.server.commitIndex=self.server.commitIndex+1
					self.server.log=log
					if data["leaderCommit"]>self.server.commitIndex:
						self.server.commitIndex=min(data["leaderCommit"], self.server.lastLogIndex())
						self.server.apply_log(self.server.commitIndex)
					self.server.leaderId=message.sender
					self.send_append_entries_response(message, True, self.server.lastLogIndex())