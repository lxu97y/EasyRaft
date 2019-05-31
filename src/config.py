class Config:
    NUMBER_TOTAL_NODES = 5
    NODE_LIST = {
        #value :(ip,publish port, client socket)
        '1':("0.0.0.0",4433,4438),
        '2':("0.0.0.0",4434,4439),
        '3':("0.0.0.0",4435,4440),
        '4':("0.0.0.0",4436,4441),
        '5':("0.0.0.0",4437,4442)
    }