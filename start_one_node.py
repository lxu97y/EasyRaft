from src.server.server import Server
from src.state.follower import Follower
from src.state.candidate import Candidate
import threading
import time
import sys

timeout = float(sys.argv[2])
log_status = int(sys.argv[3])
complete_test_log = [
    {
        "action":None,
        "term":0,
    },
    {
        "action":{'key':1,'value':1},
        "term":0,
    },
    {
        "action":{'key':1,'value':1},
        "term":0,
    },
    {
        "action":{'key':1,'value':1},
        "term":0,
    },

]

ids = []
ids = [i for i in range(1,6)]

print(complete_test_log[:log_status+1])
for i,id in enumerate(ids):
    if str(id) == sys.argv[1]:
        Server(sys.argv[1], complete_test_log[:log_status+1], 
            Follower(None), 
            [str(_) for _ in ids[:i]+ids[i+1:]],)

