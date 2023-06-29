from functools import wraps
import jwt
from flask import request, jsonify
from application import app
from application.model.databaseModel.User import User
import inspect

# TODO optional add blacklist tokens

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            bearer = request.headers.get('Authorization')  # Bearer YourTokenHere
            token = bearer.split()[1]


        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(jwt=token,key=app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            if current_user is None : return jsonify({'message': 'user is not exist'})
            else :
                # TODO Check if User class is in annotations
                if "user" in inspect.getfullargspec(f).args : return f(current_user,*args,**kwargs)
                else: return f(*args,**kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message':'Signature expired. Please log in again.'})
        except jwt.InvalidTokenError as j:
            print(j)
            return jsonify({'message':'Invalid token. Please log in again.'})
        except Exception as e:
            print(e)
            return jsonify({'message': 'token is invalid'})
    return decorator
