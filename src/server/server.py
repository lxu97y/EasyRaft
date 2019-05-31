from ..message.message import *
import time
from ..state.follower import Follower
from ..state.candidate import Candidate
from ..config import Config
from threading import Timer
import random
from collections import deque
import zmq
import threading

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
        print(self.id+" become follower")
        self.timer = None
        self.refresh_election_timer()
        self.message_buffer=deque()#to do: thread safe design
        self.buffer_lock = threading.RLock()
        self.log_lock = threading.RLock()
        self.p_thread = threading.Thread(target=self.publish_task)
        self.p_thread.start()
        self.s_thread = threading.Thread(target=self.subscribe_task)
        self.s_thread.start()
        self.l_thread = threading.Thread(target=self.listen_client)
        self.l_thread.start()
        self.kvstore=dict()

    def listen_client(self):
        context=zmq.Context()
        socket=context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:%s"%Config.NODE_LIST[self.id][2])
        while True:
            request = socket.recv_pyobj()
            response = self.state.handle_client_request(request)
            socket.send_pyobj(response)

    def apply_log(self,new_last_applied_index):
        for i in range(self.lastApplied+1,new_last_applied_index+1):
            log_entry = self.log[i]
            self.kvstore[log['action']['key']] = log['action']['value']
        self.lastApplied=new_last_applied_index

    def publish_task(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://0.0.0.0:%d" % Config.NODE_LIST[self.id][1])
        while True:
            if self.message_buffer:
                self.buffer_lock.acquire()
                message = self.message_buffer.popleft()
                self.buffer_lock.release()
                socket.send_pyobj(message)
            time.sleep(0.01)

    def subscribe_task(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        for adjacent in self.adjacents:
            socket.connect("tcp://127.0.0.1:%d" % Config.NODE_LIST[adjacent][1])

        while True:
            socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))
            message = socket.recv_pyobj()
            if message.receiver == self.id or message.receiver is None:
                self.receive_message(message)

    def refresh_election_timer(self):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(random.randrange(150,300)/1000,self._convert_to_candiate)
        self.timer.start()

    def _convert_to_candiate(self):
        print(self.id+" become candidate and start election")
        self.currentTerm+=1
        Candidate(self)#timer would be refresh when initialing the state object

    def lastLogIndex(self):
        return len(self.log)-1

    def lastLogTerm(self):
        return self.log[-1]["term"]

    def set_state(self,state):
        self.state = state
        return  

    def publish_message(self,message):
        self.buffer_lock.acquire()
        self.message_buffer.append(message)
        self.buffer_lock.release()
        return

    def receive_message(self,message):
        #call the handle_message method state
        if self.currentTerm<message.term:
            #convert to follower
            self.currentTerm=message.term
            Follower(self)
            

        self.state.handle_message(message)
        return