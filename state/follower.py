import time
import random
from ..message.message import *

class Follwer(State):
	def __init__(self):
		State.__init__(self)

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

	def send_append_entries_response(self, message, success):
		data={"success": success}
		response=AppendEntriesResponse(self.server.name, message.sender, message.term, data)
		self.server.send_response(response)

	

	