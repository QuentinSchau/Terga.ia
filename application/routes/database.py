import uuid

import datetime
import jwt
from flask import request, jsonify, make_response

from application import app, db
from application.auth import admin_required
from application.model.databaseModel.User import User


@app.route('/register', methods=['POST'])
@admin_required
def signup_user():
    data = request.get_json()

    # TODO Check user name, user email (with regex) and password to enjure that not injection
    #      Check if we have all necessery fields
    #      Check if the user don't already exist
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'],
                     admin=False,created_on=datetime.datetime.utcnow())
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(name=auth.username).first()
    if user is None : return make_response('you are not registered', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    if user.check_password(auth.password):
        user.isConnected()
        token = jwt.encode(
            payload=dict(public_id=user.public_id,
                 exp=datetime.datetime.utcnow() + datetime.timedelta(minutes=30)),
            key=app.config['SECRET_KEY'])
        return jsonify({'token': token,'message': 'connected successfully'})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
