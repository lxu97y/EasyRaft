import time
import random
from ..message.message import *
from ..state.state import State

class Candidate(object):
    """docstring for Candidate"""
    def __init__(self):
        self.received_votes=0
        self.election()

    def election(self):
        candidateId = self.server.id
        term = self.server.term
        data = {
            'lastLogIndex':len(self.server.log),
            'lastLogTerm' :self.server.log[-1]['term'] if self.server.log else 0
        }
        message = VoteRequest(candidateId, None, term, data)
        self.server.publish_message(message)
        return
    def handle_vote_response(self,message):






        