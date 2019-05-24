from server.server import Server
from state.follower import Follower

server_list=[]
ids = range(1,6)


def add_server(id,ids):
    server_list.append(Server(id, [{
            "action":"",
            "term":0,
        }], Follower(None), ids[:i]+ids[i+1:]))

for i,id in enumerate(ids):
    