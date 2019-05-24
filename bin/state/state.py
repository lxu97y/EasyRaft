import time
import random
from ..message.message import *
from ..config import Config


class State(object):
    """docstring for State"""
    def __init__(self,server=None):
        # self.timeout=random.randrange(150,300)
        self.leaderId = None
        self.server = server
        self.votedFor = None

    def set_server(self, server):
        self.server=server

    def refresh_election_timeout(self):
        self.timeout=random.randrange(150,300)

    def send_bad_response(self, message):
        data={}
        response=BadResponse(self.server.name, message.sender, message.term, data)
        self.server.send_response(response)

    def send_vote_response(self, message, voteGranted):
        data={"voteGranted": voteGranted}
        response=VoteResponse(self.server.id, message.sender, message.term, data)
        self.server.publish_message(response)

    def handle_vote_request(self,message):
        if message.term < self.server.currentTerm or "lastLogIndex" not in message.data.keys():
            self.send_vote_response(message, False)
        elif self.votedFor in [None,message.data.get('candidateId',None)] and message.data["lastLogIndex"]>= (len(self.server.log)-1):
            self.votedFor=message.sender
            self.send_vote_response(message, True)
        else:
            self.send_vote_response(message, False)

    #empty interface for child override
    def handle_vote_response(self,message):
        pass
        
    def handle_append_entries_request(self,message):
        pass

    def handle_append_entries_response(self, message):
        pass

    def handle_message(self,message):
        if message.type is None or message.term is None:
            self.send_bad_response(message)
        
        if message.type==BaseMessage.APPEND_ENTRIES_REQUEST:
            self.handle_append_entries_request(message)
        elif message.type==BaseMessage.VOTE_REQUEST:
            self.handle_vote_request(message)
        elif message.type==BaseMessage.APPEND_ENTRIES_RESPONSE:
            self.handle_append_entries_response(message)
        elif message.type == BaseMessage.VOTE_RESPONSE:
            self.handle_vote_response(message)
        elif message.type==BaseMessage.BAD_RESPONSE:
            print("ERROR! This message is bad. "+str(message))
        else:
            pass
