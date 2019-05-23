from ..message.message import *
import time
from ..state.follwer import Follower
from ..config import Config

class Server(object):
    def __init__(self, id, state, log, adjacents):
        self.id = id
        self.state = state
        self.log = log
        self.adjacents = adjacents
        self.commitIndex = 0
        self.currentTerm = 0
        self.lastApplied = 0
        self.state.set_server(self)

    def set_state(self,state):
        self.state = state

    def send_response(self,message):
        #either request to response
        pass

    def publish_message(self,message):
        pass

    def receive_message(self,message)
        #call the handle_message method state
        if self.currentTerm<message.term:
            #convert to follower
            self.set_state(Follower(self))
            self.currentTerm=message.term

        self.state.handle_message(message)