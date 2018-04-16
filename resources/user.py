from flask_restful import Resource, reqparse
import sqlite3

from models.user import UserModel

class UsersList(Resource):
    def get(self):
       return {'users': [ user.json() for user in UserModel.query.all() ] }


class User(Resource):
    def get(self, username):
        user = UserModel.find_by_username(username)

        if user is not None:
            return user.json(), 200
        return {'message': 'user was not found!'}, 404
        

class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'This fild can not be blank' 
    )

    parser.add_argument('password', 
        type = str,
        required = True,
        help = 'This filed can not be blank'
    )

    parser.add_argument('email', 
        type = str,
        required = True,
        help = 'This filed can not be blank'
    )

    def post(self):
        data = RegisterUser.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'a user with the provided username already exists'}, 400
            
        user = UserModel(None, data['username'], data['password'], data['email'])

        try:
            user.save_to_db()
        except:
            return { 'message': 'Something went wrong'}, 500

        return {'message': 'user created successfully'}, 201