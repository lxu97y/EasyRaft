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
    if i<=3:
        cl="python start_one_node.py "+str(id)+' 0.3 2'
        #https://docs.python.org/3/library/subprocess.html
        args = shlex.split(cl)
        process = subprocess.Popen(args)
        server_list.append(process)
    else:
        time.sleep(1)
        test_follower_server = Server(str(id), [
            {
                "action":None,
                "term":0,
            },
            {
                "action":None,
                "term":1,
            },
            {
                "action":None,
                "term":1,
            },
            ], Follower(None), [str(_) for _ in ids[:i]+ids[i+1:]])
    

while len(test_follower_server.log)>1:
    print(test_follower_server.log)
    time.sleep(0.1)

print("wrong extra log was removed"+str(test_follower_server.log))

while True:
    time.sleep(10)
