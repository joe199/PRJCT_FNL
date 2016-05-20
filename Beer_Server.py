from __future__ import print_function
from flask import Flask, jsonify, abort, make_response, request

Server = Flask(__name__)

#DB Session

def db_session():
    path_to_db = "mydatabase.db"
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


#Users CRUD

@app.route('/users', methods=['GET'])
def get_users():
    session = db_session()
    users = session.query(User).all()
    return jsonify({'users': users})


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    session = db_session()
    try:
        user = session.query(User).filter_by(id=user_id).one()
    except:
        abort(404)
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email)

@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'userid' in request.json or not 'username' in request.json or not 'realname' in request.json or not 'email' in request.json:
        abort(400)
    session = db_session()
    try:
        user = {
            'id': users[-1]['id'] + 1,
            'userid': request.json['userid'],
            'username': request.json['username'],
            'realname': request.json['realname'],
            'email': request.json['email'],
            'amounut': request.json['amount'],
        }
        print(User)
        session.add(user)
        session.commit()
        #user = ""
    except:
        abort(404)
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email)
    #return jsonify({'post': post}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    session = db_session()
    try:
        if not request.json:
            abort(400)
        user = session.query(User).filter_by(id=user_id).one()
        if 'userid' in request.json:
            user.userid = request.json['userid']
        if 'username' in request.json:
            user.username = request.json['username']
        if 'realname' in request.json:
            user.realname = request.json['realname']
        if 'email' in request.json:
            user.email = request.json['email']
    except:
        session.commit()
        abort(404)
    session.commit()
    return jsonify(id=user.id,userid=user.userid,username=user.username,realname=user.realname,email=user.email)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session()
    try:
        user = session.query(User).filter_by(id=user_id).one()
        session.delete(user)
        session.commit()
    except:
        abort(404)
    return jsonify({'result': True})


if __name__ == '__main__':
    Server.debug = True
    Server.run("0.0.0.0")
