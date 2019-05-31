import shlex, subprocess
import threading
import time
import sys
sys.path.append("..")
from src.server.server import Server
from src.state.follower import Follower
from src.state.candidate import Candidate

server_list=[]
ids = [i for i in range(1,6)]

threads=[]
server_list=[]

for i,id in enumerate(ids):
    if i==0:
        test_leader_server = Server(str(id), [
            {
                "action":None,
                "term":0,
            },
            {
                "action":{'key':1,'value':1},
                "term":0,
            },
            {
                "action":{'key':2,'value':2},
                "term":0,
            }
            ], Follower(None), [str(_) for _ in ids[:i]+ids[i+1:]])
    else:
        cl="python start_one_node.py "+str(id)+' 0.3 0'
        #https://docs.python.org/3/library/subprocess.html
        args = shlex.split(cl)
        process = subprocess.Popen(args)
        server_list.append(process)
    

while test_leader_server.lastApplied<2:
    print(test_leader_server.lastApplied)
    time.sleep(0.1)

print("the server has apply the latest log to state machine: "+str(test_leader_server.kvstore))


for process in server_list:
    process.terminate()