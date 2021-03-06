import zmq
from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import User, Base, Keg


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

def save_data(message):
    #Aqui guardarem el messsage rebut(que constara del NFC's id i la quantitat de birra)
    try:
        #desglosem en variables
        message1 = message.split(" ")
        userid = message1[0]
        amount = float(message1[1])
        keg = int(message1[2])
        print '\n rebut', userid, " ", amount, " ", keg
        #load session
        session = db_session()
        #primer de tot, buscar a la taula la quantitat de birra que ha vegut un id,
        #actualitzar aquest valor sumant lo que hi havia i lo nou
        user = session.query(User).filter_by(userid = userid)
        try:
           user = user.one()
        except:
           new_user = User(username='No_ident', userid=userid, realname='fantasma', email='no email', amount=amount)
           session.add(new_user)
           session.commit()

        amount_total = float(user.amount) + amount
        user.amount = amount_total
        print 'user.amount = ', user.amount
        session.commit()

            #guardem a la taula keg, la nova etrada
        keg1 = session.query(Keg).filter_by(kegid = keg).one()
        amount_total1 = float(keg1.amount) + amount
        keg1.amount = amount_total1
        print 'keg1.amount2= ', keg1.amount

        session.commit()
        return True
    except:
        return False




# Run a simple "Echo" server
while True:
    message = sock.recv()
    if message is not None:
        save = save_data(message)
    if save is True:
        sock.send("Ha estat guardat correctament")
    else:
        sock.send("No estat guardat correctament")
