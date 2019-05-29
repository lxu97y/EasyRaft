from bin.server.server import Server
from bin.state.follower import Follower
import threading
server_list=[]
ids = [i for i in range(1,6)]

threads=[]
server_list=[]

for i,id in enumerate(ids):
    t=threading.Thread(target=server_list.append,args=(Server(str(id), [{
            "action":None,
            "term":0,
        }], Follower(None), [str(_) for _ in ids[:i]+ids[i+1:]]),))
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()