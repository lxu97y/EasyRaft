import time
import random
from ..message.message import *
from ..state.state import State
class Leader(State):
    def __init__(self):
        self.nextIndex = dict()
        self.matchIndex = dict()

    def receive_append_entries_response(self,message):
        # to do
    def heartbeat()
        # to do

