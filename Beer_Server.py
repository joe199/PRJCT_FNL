from __future__ import print_function
from flask import Flask, jsonify, abort, make_response, request
from flask import redirect, url_for, render_template
from sqlalchemy_declarative import User, Keg, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

#Innit DB Session

def db_session():
    path_to_db = "beer_coholic.db"
    engine = create_engine('sqlite:///' + path_to_db)
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session


#Errors

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


#Users Web Service CRUD

@app.route('/web_service/users', methods=['GET'])
def get_users():
    session = db_session()
    users = session.query(User).all()
    all_users=[ user.__json__() for user in users]
    return jsonify({'users': all_users})

@app.route('/web_service/users/<username>', methods=['GET'])
def get_user(username):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).one()
    except:
        abort(404)
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email)

@app.route('/web_service/users', methods=['POST'])
def create_user():
    if not request.json or not 'userid' in request.json or not 'username' in request.json or not 'realname' in request.json or not 'email' in request.json:
        abort(400)
    session = db_session()
    try:
        user = User(userid=request.json['userid'], username=request.json['username'], realname=request.json['realname'], email=request.json['email'], amount=0)
        session.add(user)
    except:
        session.commit()
        abort(404)
    session.commit()
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email)

@app.route('/web_service/users/<username>', methods=['PUT'])
def update_user(username):
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
    except:
        session.commit()
        abort(404)
    session.commit()
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email)

@app.route('/web_service/users/<username>', methods=['DELETE'])
def delete_user(username):
    session = db_session()
    try:
        user = session.query(User).filter_by(username=username).one()
        session.delete(user)
        session.commit()
    except:
        abort(404)
    return jsonify({'result': True})


#Keg Web Service CRUD

@app.route('/web_service/kegs', methods=['GET'])
def get_kegs():
    session = db_session()
    kegs = session.query(Keg).all()
    all_kegs=[ keg.__json__() for keg in kegs]
    return jsonify({'kegs': all_kegs})


@app.route('/web_service/kegs/<int:kegid>', methods=['GET'])
def get_keg(kegid):
    session = db_session()
    try:
        keg = session.query(Keg).filter_by(kegid=kegid).one()
    except:
        abort(404)
    return jsonify(id=keg.id,amount=keg.amount,kegid=keg.kegid)

@app.route('/web_service/kegs', methods=['POST'])
def create_keg():
    if not request.json or not 'amount' in request.json or not 'kegid' in request.json:
        abort(400)
    session = db_session()
    try:
        keg = Keg(amount=request.json['amount'], kegid=request.json['kegid'])
        session.add(keg)
        session.commit()
    except:
        abort(404)
    return jsonify(id=keg.id,amount=keg.amount,kegid=keg.kegid)

@app.route('/web_service/kegs/<int:kegid>', methods=['PUT'])
def update_keg(kegid):
    session = db_session()
    try:
        if not request.json:
            abort(400)
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        if 'amount' in request.json:
            keg.amount = request.json['amount']
    except:
        session.commit()
        abort(404)
    session.commit()
    return jsonify(id=keg.id,amount=keg.amount,kegid=keg.kegid)

@app.route('/web_service/kegs/<int:kegid>', methods=['DELETE'])
def delete_keg(kegid):
    session = db_session()
    try:
        keg = session.query(Keg).filter_by(kegid=kegid).one()
        session.delete(keg)
        session.commit()
    except:
        abort(404)
    return jsonify({'result': True})


#Functions

def get_users_data():
    session = db_session()
    user = session.query(User).all()
    list_of_lists=[]
    for row in user:
        list_of_lists.append((row.userid,row.username,row.realname,row.email,row.amount))
    return list_of_lists

def user_exists(username):
    session = db_session()
    try:
        print (username)
        user = session.query(User).filter_by(username=username).one()
        print (user)
        session.commit()
        return True
    except:
        print ("idfhiusdhfguihysdifgh")
        session.commit()
        return False

def save_user(username,fullname,email,userid):
    if user_exists(username):
        return False
    else:
        try:
            session = db_session()
            new_user = User(username=username, realname=fullname, email=email, userid=userid)
            session.add(new_user)
            session.commit()
            return True
        except:
            return False

#Routes

@app.route('/')
def hello1():
    return render_template('landing_page1.html')

@app.route('/web_app')
def hello():
    return render_template('landing_page.html')

@app.route('/web_app/show_users', methods=['GET', 'POST'])
def hist_data():
    historical_data = get_users_data()
    return render_template('show_users_table.html',historical_data=historical_data)



@app.route('/web_app/insert_user', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('insert_user.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        userid = request.form.get('userid')
        if save_user(username,fullname,email,userid):
            return render_template('user_register_succesfully.html',username=username,realname=fullname)
        else:
            return render_template('register_error.html')


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
