import zmq
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import User, Base


# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:5678")

def db_session():
    # Create engine and bind base to it
    path_to_db = "beer_coholic.db"
    engine = create_engine('sqlite:///' + path_to_db)
    Base.metadata.bind = engine
    # Make a new session and return it
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session

def sava_data(self, message):
    #Aqui guardarem el messsage rebut(que constara del NFC's id i la quantitat de birra)
    try:
        #desglosem en variables
        message1 = message.split(" ")
        userid = message1[0]
        amount = str(message1[1])
        keg = str(message1[2])
        print userid, " ", amount, " ", keg
        #load session
        session = db_session()
        #primer de tot, buscar a la taula la quantitat de birra que ha vegut un id,
        #actualitzar aquest valor sumant lo que hi havia i lo nou
        user = session.query(User).filter_by(userid = userid).all()
        #
        amount_total = user.amount + amount
        user.amount = amount_total
        session.commit()

        #guardem a la taula keg, la nova etrada
        keg1 = session.query(Keg).filter_by(kegid = kegid).all()
        amount_total1 = keg1.amount + amount
        keg1.amount = amount_total1
        session.commit()
        return True
    except:
        return False


# Run a simple "Echo" server
while True:
    message = sock.recv()
    if message is not None:
        save = self.save_data(message)
    if save is True:
        sock.send("Ha estat guardat correctament")
    else:
        sock.send("No estat guardat correctament")
