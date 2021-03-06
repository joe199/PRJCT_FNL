
from __future__ import print_function
from flask import Flask, jsonify, abort, make_response, request
from flask import redirect, url_for, render_template
from sqlalchemy_declarative import User, Keg, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import sqlite3

app = Flask(__name__)

#INNIT DB SESSION

def db_session():
    path_to_db = "beer_coholic.db"
    engine = create_engine('sqlite:///' + path_to_db)
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session


#ERRORS

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


#FUNCTIONS FOR WEB APP

def get_users_data():
    session = db_session()
    user = session.query(User).all()
    list_of_lists=[]
    for row in user:
        list_of_lists.append((row.username, row.amount))
    return list_of_lists

def get_users_all_data(username):
    session = db_session()
    try:
        userall = session.query(User).filter_by(username=username).one()
        user = []
        user.append((userall.userid, userall.username, userall.realname, userall.email, userall.amount))
        return user
    except:
        return "ERROR"

def get_kegs_all_data(kegid):
    session = db_session()
    try:
        kegall = session.query(Keg).filter_by(kegid=kegid).one()
        keg = []
        keg.append((kegall.kegid, kegall.amount))
        return keg
    except:
        return "ERROR"

def get_kegs_data():
    session = db_session()
    keg = session.query(Keg).all()
    list_of_lists=[]
    for row in keg:
        list_of_lists.append((row.kegid,row.amount))
    return list_of_lists

def user_exists(username):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).one()
        return True
    except:
        return False

def save_user(username,fullname,email,userid):
    if user_exists(username):
        return (False, "exists")
    else:
        try:
            session = db_session()
            new_user = User(username=username, realname=fullname, email=email, userid=userid, amount=0)
            session.add(new_user)
            session.commit()
            return (True, "No error")
        except:
            return (False, "Error saving")

def keg_exists(kegid):
    session = db_session()
    try:
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        return True
    except:
        return False

def save_keg(kegid):
    if keg_exists(kegid):
        return (False, "exists")
    else:
        try:
            session = db_session()
            new_keg = Keg(kegid=kegid, amount=0)
            session.add(new_keg)
            session.commit()
            return (True, "No error")
        except:
            return (False, "Error saving")

def update_user(username,fullname,email,userid,amount):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).one()
        if userid != '':
            user.userid = userid
        if fullname != '':
            user.realname = fullname
        if email != '':
            user.email = email
        if amount != '':
            user.amount = amount
        session.commit()
        return True
    except:
        return False

def update_keg(kegid,amount):
    session = db_session()
    try:
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        keg.amount = amount
        session.commit()
        return True
    except:
        return False

def delete_user(username):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).one()
        session.delete(user)
        session.commit()
        return True
    except:
        return False

def delete_keg(kegid):
    session = db_session()
    try:
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        session.delete(keg)
        session.commit()
        return True
    except:
        return False


#CRUD (CREATE, READ, UPDATE, DELETE):


#CREATE FROM WEB SERVICE

#Create user
@app.route('/web_service/users', methods=['POST'])
def create_user_service():
    if not request.json or not 'userid' in request.json or not 'username' in request.json or not 'realname' in request.json or not 'email' in request.json:
        abort(400)
    if user_exists(request.json['username']):
        abort(400)
    session = db_session()
    try:
        user = User(userid=request.json['userid'], username=request.json['username'], realname=request.json['realname'], email=request.json['email'], amount=0)
        session.add(user)
        session.commit()
    except:
        abort(404)
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email,amount=user.amount)

#Create keg
@app.route('/web_service/kegs', methods=['POST'])
def create_keg_service():
    if not request.json or not 'amount' in request.json or not 'kegid' in request.json:
        abort(400)
    if keg_exists(request.json['kegid']):
        abort(400)
    session = db_session()
    try:
        keg = Keg(amount=request.json['amount'], kegid=request.json['kegid'])
        session.add(keg)
        session.commit()
    except:
        abort(404)
    return jsonify(id=keg.id,amount=keg.amount,kegid=keg.kegid)


#CREATE FROM WEB APP

#Create user
@app.route('/web_app/insert_user', methods=['GET', 'POST'])
def create_user_app():
    if request.method == 'GET':
        return render_template('insert_user.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        userid = request.form.get('userid')
        state, error = save_user(username,fullname,email,userid)
        if state:
            return render_template('user_register_succesfully.html',username=username,realname=fullname)
        elif error == "exists":
            return render_template('already_exists.html',username=username, user="username")
        else:
            return render_template('error.html')

#Create keg
@app.route('/web_app/insert_keg', methods=['GET', 'POST'])
def create_keg_app():
    if request.method == 'GET':
        return render_template('insert_keg.html')
    elif request.method == 'POST':
        kegid = request.form.get('kegid')
        state, error = save_keg(kegid)
        if state:
            return render_template('keg_register_succesfully.html',kegid=kegid)
        elif error == "exists":
            return render_template('already_exists.html',username=kegid, user="Keg Id")
        else:
            return render_template('error.html')

#READ FROM WEB SERVICE

#Read all users
@app.route('/web_service/users', methods=['GET'])
def read_users_service():
    session = db_session()
    users = session.query(User).all()
    all_users=[ user.__json__() for user in users]
    session.commit()
    return jsonify({'users': all_users})

#Read user
@app.route('/web_service/users/<username>', methods=['GET'])
def read_user_service(username):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).one()
        session.commit()
    except:
        abort(404)
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email,amount=user.amount)

#Read all kegs
@app.route('/web_service/kegs', methods=['GET'])
def read_kegs_service():
    session = db_session()
    kegs = session.query(Keg).all()
    all_kegs=[ keg.__json__() for keg in kegs]
    session.commit()
    return jsonify({'kegs': all_kegs})

#Read keg
@app.route('/web_service/kegs/<int:kegid>', methods=['GET'])
def read_keg_service(kegid):
    session = db_session()
    try:
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        session.commit()
    except:
        abort(404)
    return jsonify(id=keg.id,amount=keg.amount,kegid=keg.kegid)


#READ FROM WEB APP

#Read all users
@app.route('/web_app/show_users', methods=['GET', 'POST'])
def read_users_app():
    historical_data = get_users_data()
    return render_template('show_users_table.html',historical_data=historical_data)

#Read user
@app.route('/web_app/users/<username>', methods=['GET', 'POST'])
def read_user_app(username):
    users_data = get_users_all_data(username)
    return render_template('show_one_user.html',users_data=users_data)

#Read all kegs
@app.route('/web_app/show_kegs', methods=['GET', 'POST'])
def read_kegs_app():
    historical_data = get_kegs_data()
    return render_template('show_kegs_table.html',historical_data=historical_data)

#Read keg
@app.route('/web_app/kegs/<kegid>', methods=['GET', 'POST'])
def read_keg_app(kegid):
    kegs_data = get_kegs_all_data(kegid)
    return render_template('show_one_keg.html',kegs_data=kegs_data)


#UPDATE FROM WEB SERVICE

#Update user
@app.route('/web_service/users/<username>', methods=['PUT'])
def update_user_service(username):
    session = db_session()
    try:
        if not request.json:
            abort(400)
        user = session.query(User).filter_by(username=username).one()
        if 'userid' in request.json:
            user.userid = request.json['userid']
        if 'realname' in request.json:
            user.realname = request.json['realname']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'amount' in request.json:
            user.amount = request.json['amount']
        session.commit()
    except:
        abort(404)
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email,amount=user.amount)

#Update keg
@app.route('/web_service/kegs/<int:kegid>', methods=['PUT'])
def update_keg_service(kegid):
    session = db_session()
    try:
        if not request.json:
            abort(400)
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        keg.amount = request.json['amount']
        session.commit()
    except:
        abort(404)
    return jsonify(id=keg.id,amount=keg.amount,kegid=keg.kegid)


# UPDATE FROM WEB APP

#Update user
@app.route('/web_app/update_user', methods=['POST'])
def update_user_app():
    username = request.form.get('user_name')
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    userid = request.form.get('userid')
    amount = request.form.get('amount')
    if update_user(username,fullname,email,userid, amount):
        return render_template('user_update_succesfully.html', realname=fullname)
    else:
        return render_template('error.html')

#Update keg
@app.route('/web_app/update_keg', methods=['POST'])
def update_keg_app():
    kegid = request.form.get('kegid')
    amount = request.form.get('amount')
    if update_keg(kegid, amount):
        return render_template('keg_update_succesfully.html', amount=amount)
    else:
        return render_template('error.html')


#DELETE FROM WEB SERVICE

#Delete user
@app.route('/web_service/users/<username>', methods=['DELETE'])
def delete_user_service(username):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).one()
        session.delete(user)
        session.commit()
    except:
        abort(404)
    return jsonify({'result': True})

#Delete keg
@app.route('/web_service/kegs/<int:kegid>', methods=['DELETE'])
def delete_keg_service(kegid):
    session = db_session()
    try:
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        session.delete(keg)
        session.commit()
    except:
        abort(404)
    return jsonify({'result': True})


#DELETE FROM WEB APP

#Delete user
@app.route('/web_app/delete_user', methods=['POST'])
def delete_user_app():
    username = request.form.get('username')
    if delete_user(username):
        return render_template('user_delete_succesfully.html')
    else:
        return render_template('error.html')

#Delete keg
@app.route('/web_app/delete_keg', methods=['POST'])
def delete_keg_app():
    keg = request.form.get('kegid')
    if delete_keg(keg):
        return render_template('keg_delete_succesfully.html')
    else:
        return render_template('error.html')


#MAIN ROUTES

@app.route('/')
def hello1():
    return render_template('landing_page1.html')

@app.route('/web_app')
def hello():
    return render_template('landing_page.html')

@app.route('/web_service')
def hello2():
    return render_template('landing_page2.html')



if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
