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
        cl="python start_one_node.py "+str(id)+' 0.2 2'
        #https://docs.python.org/3/library/subprocess.html
        args = shlex.split(cl)
        process = subprocess.Popen(args)
        server_list.append(process)
        time.sleep(0.1)
    elif i<=3:
        cl="python start_one_node.py "+str(id)+' 0.3 0'
        #https://docs.python.org/3/library/subprocess.html
        args = shlex.split(cl)
        process = subprocess.Popen(args)
        server_list.append(process)
    else:
        test_follower_server = Server(str(id), [{
                "action":None,
                "term":0,
            }], Follower(None), [str(_) for _ in ids[:i]+ids[i+1:]])
    

while len(test_follower_server.log)<2:
    time.sleep(0.1)

print("new log from leader has been appended to follower"+str(test_follower_server.log))

while test_follower_server.commitIndex<2:
    time.sleep(0.1)
print("follower commitIndex has been updated due to leader's commitIndex")

while test_follower_server.lastApplied<2:
    time.sleep(0.1)

print("log was applied to state machine: "+str(test_follower_server.kvstore))


for process in server_list:
    process.terminate()
