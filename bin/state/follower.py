import time
import random
from ..message.message import *
from ..state.state import State
from ..config import Config


class Follower(State):
	def __init__(self,server=None):
		State.__init__(self, server)

	def send_append_entries_response(self, message, success):
		data={"success": success}
		response=AppendEntriesResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	def handle_append_entries_request(self, message):
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

				if len(log)>0 and log[data["prevLogIndex"]]["term"]!=data["prevLogTerm"]:
					log=log[:data["prevLogIndex"]]
					self.server.log=log
					self.server.lastLogTerm=data["prevLodTerm"]
					self.send_append_entries_response(message, False)
				else:
					if len(log)>0 and data["leaderCommit"]>0 and log[data["leaderCommit"]]["term"]!=message.term:
						log=log[:self.server.commitIndex]
						for x in data["entries"]:
							log.append(x)
							self.server.commitIndex=self.server.commitIndex+1
						self.server.log=log
						self.server.lastLogTerm=log[-1]["term"]
						self.commitIndex=len(log)-1
					elif len(data["entries"])>0:
						for x in data["entries"]:
							loag.append(x)
							self.server.commitIndex=self.commitIndex+1
						self.server.log=log
						self.server.lastLogTerm=log[-1]["term"]
						self.commitIndex=len(log)-1
					self.send_append_entries_response(message, True)