import time
import random
from ..message.message import *

class State(object):
    """docstring for State"""
    def __init__(self):
        self.timeout=random.randrange(150,300)
        self.server = None
        self.votedFor = None

    def set_server(self, server):
        self.server=server

    def refresh_timeout(self):
        self.timeout=random.randrange(150,300)

    def handle_message(self,message):
        if message.type is None or message.term is None:
            self.send_bad_response(message)
        m_type=message.type
        if message.term>self.server.currentTerm:
            self.server.currentTerm=term
            #to do : convert to follower
        elif message.term<self.server.currentTerm:
            self.send_bad_response(message)

        if m_type==BaseMessage.APPEND_ENTRIES_REQUEST:
            self.handle_append_entries(message)
        elif m_type==BaseMessage.VOTE_REQUEST:
            self.handle_vote_request(message)
        elif m_type==BaseMessage.BAD_RESPONSE:
            print("ERROR! This message is bad. "+str(message))
        else:
            pass

    def send_bad_response(self, message):
        data={}
        response=BadResponse(self.server.name, message.sender, message.term, data)
        self.server.send_response(response)


    def handle_vote_request(self,message):
        if message.term < self.server.currentTerm or "lastLogIndex" not in message.data.keys():
            self.send_vote_response(message, False)
        elif self.votedFor in [None,message.data.get('candidateId',None)] and message.data["lastLogIndex"]>= (len(self.server.log)-1):
            self.votedFor=message.sender
            self.send_vote_response(message, True)
        else:
            self.send_vote_response(message, False)

    def send_vote_response(self, message, voteGranted):
        data={"voteGranted": voteGranted}
        response=VoteResponse(self.server.name, message.sender, message.term, data)
        self.server.send_response(response)