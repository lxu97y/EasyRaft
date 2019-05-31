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
        if server:
            self.server.set_state(self)
        
    def set_server(self, server):
        self.server=server

    def send_bad_response(self, message):
        data={}
        response=BadResponse(self.server.name, message.sender, message.term, data)
        self.server.send_response(response)

    def send_vote_response(self, message, voteGranted):
        data={"voteGranted": voteGranted}
        response=VoteResponse(self.server.id, message.sender, message.term, data)
        if not voteGranted:
            print(response.sender+" refuse to vote "+response.receiver)
        else:
            print(response.sender+" vote "+response.receiver+' term is '+str(self.server.currentTerm))
        self.server.publish_message(response)

    def handle_vote_request(self,message):
        if message.term < self.server.currentTerm or "lastLogIndex" not in message.data.keys():
            self.send_vote_response(message, False)
        elif self.votedFor is None or self.votedFor == message.sender and message.data["lastLogIndex"]>= (len(self.server.log)-1):
            self.votedFor=message.sender
            if self.server.state==self:
                self.send_vote_response(message, True)
            else:
                self.send_vote_response(message, False)
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
            return
        
        self.server.refresh_election_timer()
        # print(str(self.server.id+ ' receive ')+str(message.type))

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

    def handle_client_request(self, request):
        if self.leaderId:
            response = ServerResponse(
                '300',
                {
                    'ip_address':Config.NODE_LIST[self.leaderId][0],
                    'port':Config.NODE_LIST[self.leaderId][1],
                }
                    )
        else:
            response = ServerResponse('500',{})
        return response