import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask import jsonify

from resources.item import Item, Itemlist
from resources.user import UserRegister
from security import authenticate, identity as identity_function
from flask_cors import CORS

import os
from datetime import timedelta 


app = Flask(__name__)
app.secret_key = 'AR'
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_AUTH_URL_RULE'] = '/login' #change the URL

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'


#jwt = JWT(app, authenticate, identity_function)   #/auth
jwt = JWT(app, authenticate, identity_function)   #/auth

api.add_resource(Item, '/item/<string:name>')   # /student/Rolf
api.add_resource(Itemlist, '/items')
#api.add_resource(UserRegister, '/register/<string:name>')
api.add_resource(UserRegister, '/register', '/register/<string:name>')


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
 return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
     })

@jwt.jwt_error_handler
def customized_error_handler(error):
 return jsonify({
        'message': error.description,
        'code': error.status_code
        }), error.status_code

#app.run(host = '0.0.0.0', port = 5000, debug=True)
if __name__ == '__main__':  
       app.run(host = '0.0.0.0', port=os.environ.get('PORT'), debug=True)