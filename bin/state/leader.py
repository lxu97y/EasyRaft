import time
import random
from ..message.message import *
from ..state.state import State
from ..config import Config
from collections import defaultdict

class Leader(State):
    def __init__(self,server=None):
        State.__init__(self,server)
        self.matchIndex = defaultdict(int)
        self.nextIndex = defaultdict(int)
        for adjacent in self.server.adjacents:
            self.nextIndex[adjacent] = self.server.lastLogIndex()+1
        if self.server.timer:
            self.server.timer.cancel()
        self.heartbeat()

    def handle_vote_request(self,message):
    #method override, leader should refuse any vote request unless the one from newer term(in this case it should convert to follower)
        self.send_vote_response(message, False)

    def handle_append_entries_response(self,message):
        if message.data['success']:
            self.matchIndex[message.sender]=message.data['matchIndex']
            self.nextIndex[message.sender] = message.data['matchIndex']+1
            self._update_match_index()
        else:
            self.nextIndex[message.sender]-=1
        # to do
    def _update_commit_index(self):
        match_index_array = sorted(self.matchIndex.values())
        for i,matchIndex in enumerate(match_index_array):
            if matchIndex> self.server.matchIndex:
                if len(match_index_array)-i+1>=(len(match_index_array)/2):
                    self.server.matchIndex = matchIndex
                return

    def heartbeat(self):
        while True:
            for adjacent in self.server.adjacents:
                self.server.log_lock.acquire()
                data={
                'prevIndex':self.server.lastLogIndex(),
                'prevTerm':self.server.lastLogTerm(),
                'entries':[],
                'commitIndex':self.server.commitIndex
                }
                self.server.log_lock.release()
                if self.server.lastLogIndex()>=self.nextIndex[adjacent]:
                    data['prevIndex']=self.nextIndex[adjacent]-1
                    data['prevTerm']=self.server.log[data['prevIndex']]['term']
                    data['entries']=self.server.log[self.nextIndex[adjacent]:self.server.lastLogIndex()+1]

                message = AppendEntriesRequest(self.server.id, adjacent, self.server.currentTerm, data)
                self.server.publish_message(message)
            time.sleep(0.005)
    
    def handle_client_request(self):
        pass