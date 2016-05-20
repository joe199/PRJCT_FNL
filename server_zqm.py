import zmq


# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:5678")


def sava_data(self, message):
    pass
    #Aqui guardarem el messsage rebut(que constara del NFC's id i la quantitat de birra)









# Run a simple "Echo" server
while True:
    message = sock.recv()
    if message is not None:
        self.save_data(message)
    sock.send("Ha estat guardat correctament")
