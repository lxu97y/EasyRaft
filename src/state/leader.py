import time
import random
from ..message.message import *
from ..state.state import State
from ..config import Config
from collections import defaultdict
import threading

class Leader(State):
    def __init__(self,server=None):
        State.__init__(self,server)
        self.matchIndex = defaultdict(int)
        self.nextIndex = defaultdict(int)
        for adjacent in self.server.adjacents:
            self.nextIndex[adjacent] = self.server.lastLogIndex()+1
            self.matchIndex[adjacent] =0
        if self.server.timer:
            self.server.timer.cancel()
        self.h_thread = threading.Thread(target=self.heartbeat)
        self.h_thread.start()

    def handle_vote_request(self,message):
    #method override, leader should refuse any vote request unless the one from newer term(in this case it should convert to follower)
        self.send_vote_response(message, False)

    def handle_append_entries_response(self,message):
        if message.data['success']:
            self.matchIndex[message.sender]=message.data['matchIndex']
            self.nextIndex[message.sender] = message.data['matchIndex']+1
            self._update_commit_index()
        else:
            print("receive false response from "+message.sender)
            #in case the false response is delayed to, the burst false response would not corrupt nextIndex
            self.nextIndex[message.sender]=max(1,self.nextIndex[message.sender]-1)

    def _update_commit_index(self):
        match_index_array = sorted(self.matchIndex.values())
        for i,matchIndex in enumerate(match_index_array):
            if matchIndex> self.server.commitIndex:
                if len(match_index_array)-i>=(len(match_index_array)/2):
                    self.server.commitIndex = matchIndex
                    self.server.apply_log(self.server.commitIndex)
                return

    def heartbeat(self):
        while True:
            for adjacent in self.server.adjacents:
                self.server.log_lock.acquire()
                data={
                'prevLogIndex':self.server.lastLogIndex(),
                'prevLogTerm':self.server.lastLogTerm(),
                'entries':[],
                'leaderCommit':self.server.commitIndex
                }
                self.server.log_lock.release()
                if self.server.lastLogIndex()>=self.nextIndex[adjacent]:
                    data['prevLogIndex']=self.nextIndex[adjacent]-1
                    data['prevLogTerm']=self.server.log[data['prevLogIndex']]['term']
                    data['entries']=self.server.log[self.nextIndex[adjacent]:self.server.lastLogIndex()+1]
                message = AppendEntriesRequest(self.server.id, adjacent, self.server.currentTerm, data)
                self.server.publish_message(message)
            time.sleep(0.1)
    
    def handle_client_request(self, request):
        if request.type=='GET':
            key = request.payload['key']
            if key in self.server.kvstore:
                return ServerResponse('200',{'value':self.server.kvstore[key]})
            else:
                return ServerResponse('400',{})
        elif request.type == 'PUT':
            self.server.log.append({'action':request.payload,'term':self.server.currentTerm})
            time.sleep(0.3)#wait the log to be applied
            index =self.server.lastLogIndex()
            if self.server.lastApplied>= index:
                return ServerResponse('200',{})
            else:
                return ServerResponse('400',{})
        return response