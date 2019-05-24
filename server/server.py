from ..message.message import *
import time
from ..state.follwer import Follower
from ..config import Config
from threading import Timer
import random
from collections import deque
import zmq

class Server(object):
    def __init__(self, id, log, state, adjacents):
        self.id = id
        self.state = state
        self.log = log #log is initialized with 0 index filled
        self.adjacents = adjacents
        self.commitIndex = 0
        self.currentTerm = 0
        self.lastApplied = 0
        self.state.set_server(self)
        self.timer = None
        self.message_buffer=deque()
        self.p_thread = threading.Thread(target=publish_task)
        self.p_thread.start()
        self.s_thread = threading.Thread(target=subscribe_task)
        self.s_thread.start()

    def publish_task(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:%d" % Config.NODE_LIST[id][1])
        while True:
            if self.message_buffer:
                message = self.message_buffer.popleft()
                socket.send(message)
            time.sleep(0.01)

    def subscribe_task(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        for adjacent in adjacents:
            socket.connect("tcp://%s:%d" % Config.NODE_LIST[id])

        while True:
            message = socket.recv()
            self.receive_message(message)


    def refresh_eletion_timer():
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(random.randrange(0.15,0.3),_convert_to_candiate)

    def _convert_to_candiate():
        self.refresh_election_timer()
        self.currentTerm+=1
        self.set_state(Candidate(self))

    def lastLogIndex(self):
        return len(self.log)-1

    def lastLogTerm(self):
        return self.log[-1]["term"]

    def set_state(self,state):
        self.state = state
        return

    def send_response(self,message):
    
        pass

    def publish_message(self,message):
        self.message_buffer.append(message)
        return

    def receive_message(self,message)
        #call the handle_message method state
        if self.currentTerm<message.term:
            #convert to follower
            self.set_state(Follower(self))
            self.currentTerm=message.term

        self.state.handle_message(message)
        return

