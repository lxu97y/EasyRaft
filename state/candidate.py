import time
import random
from ..message.message import *
from ..state.state import State
from ..server.server import Server
from ..config import Config

class Candidate(object):
    """docstring for Candidate"""
    def __init__(self,server=None):
        State.__init__(self, server)
        self.received_votes={}
        self.votedFor = self.server.id
        self.election_request()

    def election_request(self):
        candidateId = self.server.id
        term = self.server.term
        data = {
            'lastLogIndex':len(self.server.log),
            'lastLogTerm' :self.server.log[-1]['term'] if self.server.log else 0
        }
        
        message = VoteRequest(candidateId, None, term, data)
        self.server.publish_message(message)

    def handle_vote_response(self,message):
        if message.term>self.server.currentTerm:
            return #Before calling this method, the state should be convert to Follower
        elif message.term==self.server.currentTerm:
            if message.data['voteGranted']:
                self.received_votes[message.sender]=1
            else:
                pass
        if type(self.server.state)==Candidate and 2*sum(self.received_votes.values())>Config.NUMBER_TOTAL_NODES:
            #promote to leader
            self.server.set_state(Leader(self.server))