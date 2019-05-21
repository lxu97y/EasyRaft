from ..message.message import *
import time

NUMBER_TOTAL_NODES =5

class Server(object):
    def __init__(self, id, state, log, neighbors):
        self.id = id
        self.state = state
        self.log = log
        self.neighbors = neighbors
        self.commitIndex = 0
        self.currentTerm = 0
        self.lastApplied = 0
        self.state.set_server(self)
    def send_response(self,message):
        #either request to response
    def send_response(self,message):

    def receive_message(self,message)
        #call the handle_message method state
        if self.currentTerm<= message.term:
            self.state.handle_message(message)
        else:
            #send bad response