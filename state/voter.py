import time
import random
from ..message.message import *
class Voter(object):
    """docstring for Voter"""
    def __init__(self, ):
        self.votedFor = None

    def handle_vote_request(self,messgae):
        if "lastLogIndex" not in message.data.keys():
            self.send_vote_response(message, False)
        if self.votedFor is None and message.data["lastLogIndex"]>= (len(self.server.log)-1):
            self.votedFor=message.sender
            self.send_vote_response(message, True)
        else:
            self.send_vote_response(message, False)
    def send_vote_response(self, message, voteGranted):
        data={"voteGranted": voteGranted}
        response=VoteResponse(self.server.name, message.sender, message.term, data)
        self.server.send_response(response)