from functools import wraps
import jwt
from flask import request, jsonify
from application import app
from application.model.databaseModel.User import User
import inspect

# TODO optional add blacklist tokens

def checkConnexionToken():
    '''
    Method which checks that a token has been passed in the request header.
    It also checks whether the token is valid.
    If so, the user is returned, otherwise it returns an error.
    :param func: function to execute if token is valid.
    :return: The current user found by their token or a dict which contains the error's message
    '''
    token = None
    if 'Authorization' in request.headers:
        bearer = request.headers.get('Authorization')  # Bearer YourTokenHere
        token = bearer.split()[1]
    if not token:
        return jsonify({'message': 'a valid token is missing'})
    try:
        data = jwt.decode(jwt=token, key=app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.filter_by(public_id=data['public_id']).first()
        if current_user is None:
            return jsonify({'message': 'user is not exist'})
        else:
            return current_user
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Signature expired. Please log in again.'})
    except jwt.InvalidTokenError as j:
        print(j)
        return jsonify({'message': 'Invalid token. Please log in again.'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'token is invalid'})

def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        current_user = checkConnexionToken()
        # if we have not a user, it's an error and we return it
        if not isinstance(current_user,User):
            return current_user
        else:
            # TODO Check if User class is in annotations
            if "user" in inspect.getfullargspec(func).args and isinstance(inspect.getfullargspec(func).annotations['user'],User.__class__):
                return func(current_user, *args, **kwargs)
            else:
                return func(*args, **kwargs)
    return decorator

def admin_required(func):
    '''
    Method that checks that the user has sent a token and has admin privileges
    :param func: function to execute
    :return:
    '''
    @wraps(func)
    def decorator(*args, **kwargs):
        current_user = checkConnexionToken()
        # if we have not a user, it's an error and we return it
        if not isinstance(current_user, User):
            return current_user
        else:
            if current_user.admin:
                # TODO Check if User class is in annotations
                if "user" in inspect.getfullargspec(func).args and isinstance(inspect.getfullargspec(func).annotations['user'],User.__class__):
                    return func(current_user, *args, **kwargs)
                else:
                    return func(*args, **kwargs)
            else:
                return jsonify({'message': 'You have not admin privilege'})
    return decorator