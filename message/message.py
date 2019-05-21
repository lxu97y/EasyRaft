class BaseMessage(object):
	APPEND_ENTRIES_REQUEST=1
	APPEND_ENTRIES_RESPONSE=2
	VOTE_REQUEST=3
	VOTE_RESPONSE=4

	def __init__(self, sender, receiver, term, data):
		self.sender=sender
		self.receiver=receiver
		self.term=term
		self.data=data

class AppendEntriesRequest(BaseMessage):
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.APPEND_ENTRIES_REQUEST

class AppendEntriesResponse(BaseMessage):
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.APPEND_ENTRIES_RESPONSE

class VoteRequest(BaseMessage):
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.VOTE_REQUEST

class VoteReponse(BaseMessage):
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.VOTE_RESPONSE