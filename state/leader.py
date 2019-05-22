import time
import random
from ..message.message import *
from ..state.state import State
from ..server.server import Server
from ..config import Config


class Leader(State):
    def __init__(self,server=None):
        State.__init__(self,server)
        self.nextIndex = dict()
        self.matchIndex = dict()

    def receive_append_entries_response(self,message):
        pass
        # to do
    def heartbeat():
        pass
        # to do

