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
        cl="python start_one_node.py "+str(id)+' 0.1 0'
        #https://docs.python.org/3/library/subprocess.html
        args = shlex.split(cl)
        process = subprocess.Popen(args)
    else:
        t=threading.Thread(target=server_list.append,args=(Server(str(id), [{
                "action":None,
                "term":0,
            }], Follower(None), [str(_) for _ in ids[:i]+ids[i+1:]]),))
        t.start()
        threads.append(t)

time.sleep(3)
print('kill leader')
process.terminate() 
for thread in threads:
    thread.join()