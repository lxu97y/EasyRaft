from src.server.server import Server
from src.state.follower import Follower
from src.state.candidate import Candidate
import threading
import time
import shlex, subprocess

server_list=[]
ids = [i for i in range(1,6)]

threads=[]
server_list=[]

for i,id in enumerate(ids):
    if i==0:
        cl="python start_one_node.py "+str(id)+' 0.2 1'
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
    

while len(test_follower_server.log)==1:
    time.sleep(0.1)

print("Append one entries from leader")

for process in server_list:
    process.terminate()