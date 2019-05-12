import socket
import json
import sys
import threading


kv_store=dict()

def main():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("0.0.0.0", int(sys.argv[1])))
	server_socket.listen(5)

	while True:
		(accepted_socket,addr) = server_socket.accept()
		new_thread = threading.Thread(target=task,args=(accepted_socket,))
		new_thread.start()


def task(accepted_socket):
	data = accepted_socket.recv(1024)
	json_package = data.decode('utf8')
	response=parse(json_package)
	accepted_socket.send(response.encode('utf8'))
	accepted_socket.close()

def parse(json_package):
	action=json.loads(json_package)
	action_type=action['type']
	payload=action['payload']
	response=None
	if action_type=='put':
		response=put(payload)
	elif action_type=='get':
		response=get(payload)
	else:
		response=undefinedAction()
	return json.dumps(response)



def put(payload):
    #input payload
    #return dict of reply
    key = payload['key']
    if not key:#empty key
        return {'code':'fail','payload':{'message':'empty key','key':key,'value':kv_store[key]}}
        
    value = payload['value']
    kv_store['key']=value
    return {'code':'success'}

def get(payload):
    key = payload['key']
    if key not in kv_store:
        return {'code':'fail'}
    else:
        return {'code':'success','payload':{'message':'','key':key,'value':kv_store[key]}}

def undefinedAction():
	response={'code':'undefined action'}
	return response

if __name__=="__main__":
    main()