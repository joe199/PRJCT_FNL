import zmq
import sys

class client_sensor():


    def enviar(uid, quantitybeer, sortidor):

        context = zmq.Context()

        # Define the socket using the "Context"
        sock = context.socket(zmq.REQ)
        sock.connect("tcp://127.0.0.1:5678")

        # Send a "message" using the socket
        parametres = str(uid)+ " "  + str(quantitybeer) + " " + str(sortidor)
        sock.send(parametres)
        print sock.recv()
        return True
