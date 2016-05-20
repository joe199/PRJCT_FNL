from datetime import datetime, date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import User, Base, Keg


def db_session():
    # Create engine and bind base to it
    path_to_db = "beer_coholic.db"
    engine = create_engine('sqlite:///' + path_to_db)
    Base.metadata.bind = engine
    # Make a new session and return it
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session

def crear_users():

    try:
        #load session
        session = db_session()
        #saving user
        new_user = User(username=username, userid=userid, realname=realname, email=email, amount=amount)
        session.add(new_user)
        session.commit()
        print "User, Perfecte"
    except:
        print "User, Malament"

def crear_kegs():

    try:
        #load session
        session = db_session()
        #saving user
        new_user = Keg(amount=amount, kegid=kegid)
        session.add(new_user)
        session.commit()
        print "Keg, Perfecte"
    except:
        print "keg, Malament"


if __name__ == '__main__':
    crear_users()
    crear_kegs()
