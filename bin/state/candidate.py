import time
import random
from ..message.message import *
from ..state.state import State
from ..config import Config
from ..state.leader import Leader

class Candidate(State):
    """docstring for Candidate"""
    def __init__(self,server=None):
        State.__init__(self, server)
        self.received_votes={self.server.id:1}
        self.votedFor = self.server.id
        self.server.refresh_election_timer()
        self.election_request()

    def election_request(self):
        candidateId = self.server.id
        term = self.server.currentTerm
        data = {
            'lastLogIndex':self.server.lastLogIndex(),
            'lastLogTerm' :self.server.lastLogTerm()
        }
        
        message = VoteRequest(candidateId, None, term, data)
        self.server.publish_message(message)
        return

    def handle_vote_response(self,message):
        if message.term>self.server.currentTerm:
            return #Before calling this method, the state should be convert to Follower
        elif message.term==self.server.currentTerm:
            if message.data['voteGranted']:
                self.received_votes[message.sender]=1
            else:
                self.received_votes[message.sender]=0
        if type(self.server.state)==Candidate and 2*sum(self.received_votes.values())>Config.NUMBER_TOTAL_NODES:
            #promote to leader
            print(self.server.id+"become leader"+'\ncurrent term is '+str(self.server.currentTerm)
                + "vote detail: "+str(self.received_votes))
            self.server.set_state(Leader(self.server))
        return














        