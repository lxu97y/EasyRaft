import time
import random
from ..message.message import *
from ..state.state import State
from ..config import Config


class Leader(State):
    def __init__(self,server=None):
        State.__init__(self,server)
        self.nextIndex = dict()
        self.matchIndex = dict()
        self.heartbeat

    def receive_append_entries_response(self,message):
        pass
        # to do
    def heartbeat(self):
        while True:
            data={
                'prevIndex':0,
                'prevTerm':0,
                'entries':[],
                'commitIndex':0
            }
            message = AppendEntriesRequest(self.server.id, None, self.server.currentTerm, data)
            self.server.publish_message(message)
            time.sleep(0.005)