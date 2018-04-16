from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import sqlite3

from models.todo import TodoModel

class TodosList(Resource):
    @jwt_required()
    def get(self):
       return { 'todos': [ todo.json() for todo in TodoModel.query.all() ] }


class Todo(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('text',
        type = str,
        required = True,
        help = 'This filed can not be blank'
    )
    parser.add_argument('done',
        type = bool
    )

    @jwt_required()
    def get(self, id):
        id = TodoModel.is_valid_id(id)

        if id == False:
            return {'message': 'invalid id'}, 400
        
        todo = TodoModel.find_by_id(id)

        if not todo:
            return {'message': 'todo was not found'}, 404
        
        current_user = current_identity

        if not todo.check_autherized(current_user.username):
            return {'message' :'not authorized to modify this todo'}, 401

        return todo.json()
    
    @jwt_required()
    def post(self, id):
        user = current_identity
        data = Todo.parser.parse_args()
        todo = {'username': user.username, 'text': data['text'], 'done': False}
        todo = TodoModel(None, user.username, data['text'], False) 
        todo.save_to_db()
        return {'message': 'todo has been created'}, 201

    @jwt_required()
    def delete(self, id):
        id = TodoModel.is_valid_id(id)
        if id == False:
            return {'message': 'invalid id'}, 400
        
        todo = TodoModel.find_by_id(id)
        if not todo:
            return {'message': 'todo was not found'}, 400
        
        current_user = current_identity 

        if not todo.check_autherized(current_user.username):
            return {'message' :'not authorized to modify this todo'}, 401

        try: 
            todo.delete_from_db()
        except:
            return {'message': 'something went wrong'}, 500
        
        return {'message': 'Deleted'}, 200
        
        
    @jwt_required()
    def put(self, id):
        id = TodoModel.is_valid_id(id)
        data = Todo.parser.parse_args()

        if id == False:
            return {'message': 'invalid id'}, 400
        
        todo = TodoModel.find_by_id(id)

        current_user = current_identity

        if not todo:
            todo = TodoModel(id, current_user.username, data['text'], False)
            todo.save_to_db()
            return {'message': 'Saved a new todo'}, 201
        
         
        if not todo.check_autherized(current_user.username):
            return {'message' :'not authorized to modify this todo'}, 401

        todo.text = data.text
        todo.done = data.done

        todo.save_to_db()

        return {'message': 'updated'}
        