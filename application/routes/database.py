import uuid

import datetime
import jwt
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from application import app, db
from application.model.databaseModel.User import User


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    # TODO Check user name, user email (with regex) and password to enjure that not injection
    # check if we have all necessery fields
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password,
                     admin=False,created_on=datetime.datetime.utcnow())
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(name=auth.username).first()
    if user is None : make_response('you are not registered', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            payload=dict(public_id=user.public_id,
                 exp=datetime.datetime.utcnow() + datetime.timedelta(minutes=30)),
            key=app.config['SECRET_KEY'])
        return jsonify({'token': token,'message': 'connected successfully'})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
