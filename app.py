from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
import datetime

from security import authenticate, identity
from resources.todo import Todo, TodosList
from resources.user import User, UsersList, RegisterUser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'ahmed'
api = Api(app)



jwt = JWT(app, authenticate, identity)
 
# configration for SQLALCHEMT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=365)

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

api.add_resource(TodosList, '/todos/')
api.add_resource(Todo, '/todo/<string:id>')
api.add_resource(UsersList, '/users/')
api.add_resource(User, '/user/<string:username>')
api.add_resource(RegisterUser, '/user/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)