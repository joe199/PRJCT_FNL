from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, primary_key=True)
    userid = Column(Integer)
    realname = Column(String)
    email = Column(String)
    amount = Column(Integer)

    def __repr__(self):
        return "<User(username='%s', userid='%s', realname='%s', email='%s', amount='%s')>" % (
                             self.username, self.userid, self.realname, self.email, self.amount)

    def __json__(self):
        userjs = {}
        userjs["id"] = self.id
        userjs["userid"] = self.userid
        userjs["username"] = self.username
        userjs["realname"] = self.realname
        userjs["email"] = self.email
        userjs["amount"] = self.amount
        return userjs

class Keg(Base):
    __tablename__ = 'keg'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    kegid = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<User(amount='%s', kegid='%s')>" % (
                             self.amount, self.kegid)

    def __json__(self):
        kegjs = {}
        kegjs["id"] = self.id
        kegjs["amount"] = self.amount
        kegjs["kegid"] = self.kegid
        return kegjs


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
from sqlalchemy import create_engine
path_to_db = "beer_coholic.db"
engine = create_engine('sqlite:///' + path_to_db)
Base.metadata.create_all(engine)
