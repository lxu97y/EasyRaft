from src.server.server import Server
from src.state.follower import Follower
from src.state.candidate import Candidate
import threading
import time
server_list=[]
ids = [i for i in range(1,6)]

threads=[]
server_list=[]

for i,id in enumerate(ids):
    if i==0:
        t=threading.Thread(target=server_list.append,args=(Server(str(id), [{
                "action":None,
                "term":0,
            }], Follower(None), [str(_) for _ in ids[:i]+ids[i+1:]],0.15),))
        t.start()
    else:
        t=threading.Thread(target=server_list.append,args=(Server(str(id), [{
                "action":None,
                "term":0,
            }], Follower(None), [str(_) for _ in ids[:i]+ids[i+1:]]),))
        t.start()
    threads.append(t)

for thread in threads:
    thread.join()
