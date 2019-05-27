class BaseMessage(object):
	'''Base messsage.
	
	This class is a wrapper class of necessary information. It is the subclass of the following four messages.
	And it contains four kinds of constant variables to indicate the type of messages. 

	Attributes:
		sender: A string, which represents the message's sender.
		receiver: A string, which represents the message's receiver.
		term: An integer, which represents the message's term.
		data: An dictionary, which contains other information. 
	'''
	APPEND_ENTRIES_REQUEST=1
	APPEND_ENTRIES_RESPONSE=2
	VOTE_REQUEST=3
	VOTE_RESPONSE=4
	BAD_RESPONSE=5

	def __init__(self, sender, receiver, term, data):
		self.sender=sender
		self.receiver=receiver
		self.term=term
		self.data=data

class AppendEntriesRequest(BaseMessage):
	'''Append entries request

	This class represents the request to append entries.

	Attributes:
		sender, receiver, term: Please see above explainations.
		data: {
			"leaderId": an integer to let follower redirect clients.
			"prevLogIndex": an integer, index of log entry immediately preceding new ones.
			"prevLogTerm": an integer, term of prevLogIndex entry
			"entries": a list, log entries to store (empty for heartbeat; may send more than one for efficiency)
			"leaderCommit": an integer, leader’s commit index
			}
	'''
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.APPEND_ENTRIES_REQUEST

class AppendEntriesResponse(BaseMessage):
	'''Append entries response

	This class represents the response to append entries.

	Attributes:
		sender, receiver, term: Please see above explainations.
		data: {
			"success": a boolean, true if follower contained entry matching prevLogIndex and prevLogTerm.
		}
	'''
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.APPEND_ENTRIES_RESPONSE

class VoteRequest(BaseMessage):
	'''Vote request

	This class represents the request to append entries.

	Attributes:
		sender, receiver, term: Please see above explainations.
		data: {
			"candidateId": an integer, candidate requesting vote.
			"lastLogIndex": an integer, index of candidate’s last log entry.
			"lastLogTerm": an integer, term of candidate’s last log entry.
		}
	'''
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.VOTE_REQUEST

class VoteResponse(BaseMessage):
	'''Vote response

	This class represents the response to vote.

	Attributes:
		sender, receiver, term: Please see above explainations.
		data: {
			"voteGranted": a boolean, true means candidate received vote.
		}
	'''
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.VOTE_RESPONSE

class BadResponse(BaseMessage):
	def __init__(self, sender, receiver, term, data):
		BaseMessage.__init__(self, sender, receiver, term, data)
		self.type=BaseMessage.BAD_RESPONSE