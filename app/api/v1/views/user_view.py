from flask import jsonify, request, make_response, Response, json
from ..schemas.user_schema import UserSchema
from ..models.user_model import User
from ..models.token_model import RevokedTokenModel
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                             get_jwt_identity, jwt_refresh_token_required, get_raw_jwt)
from flask_restful import Resource

db = User()

class Index(Resource):
    """ Resource for index endpoint """
    
    def get(self):
        return {'status': 200, 'message': 'Welcome to Questioner'}, 200

class Register(Resource):
    """ Resource to register new user """

    def post(self):
        """ Endpoint to register user """

        register_data = request.get_json()

        if not register_data:
            return {'status': 400, 'message': 'No data provided'}, 400

        try:
            data = UserSchema().load(register_data)
        except ValidationError as errors:
            return {'status': 400, 'message' : 'Invalid data. Please fill all required fields', 'errors': errors.messages}, 400

        if next(filter(lambda u: u['username'] == data['username'], db.all()), None):
            return {'status': 409, 'message' : 'Username already exists'}, 409

        if db.exists('email', data['email']):
            return {'status': 409, 'message' : 'Email already exists'}, 409

        new_user = db.save(data)
        result = UserSchema(exclude=['password']).dump(new_user)

        access_token = create_access_token(identity=new_user['id'], fresh=True)
        refresh_token = create_refresh_token(identity=new_user['id'])
        return {
            'status': 201,
            'message' : 'User created successfully',
            'data': result,
            'access_token' : access_token,
            'refresh_token' : refresh_token
        }, 201

class Login(Resource):
    """ Resource to login existing user """

    def post(self):
        """ Endpoint to login user """

        login_data = request.get_json()

        if not login_data:
            return {'status': 400, 'message': 'No data provided'}, 400

        try:
            data = UserSchema().load(login_data, partial=True)
        except ValidationError as errors:
            return {'status': 400, 'message': 'Invalid data. Please fill all required fields', 'errors': errors.messages}, 400

        try:
            username = data['username']
            password = data['password']
        except:
            return {'status': 400, 'message': 'Invalid credentials'}, 400

        if not db.exists('username', username):
            return {'status': 404, 'message' : 'User not found'}, 404

        user = db.find('username', username)

        db.checkpassword(user['password'], password)

        access_token = create_access_token(identity=user['id'], fresh=True)
        refresh_token = create_refresh_token(identity=True)
        return {
            'status': 200,
            'message': 'User logged in successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user['id']
        }, 200

class RefreshToken(Resource):
    """ Resource to refresh access token """

    @jwt_refresh_token_required
    def post(self):
        """ Endpoint to refresh user access token """

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'status': 200, 'message': 'Token refreshed successfully', 'access_token': access_token}

class Logout(Resource):
    """ Resource to logout user """

    @jwt_required
    def post(self):
        """ Endpoint to logout user """

        user_jti = get_raw_jwt()['jti']

        RevokedTokenModel().add(user_jti)
        return {'status': 200, 'message': 'Logged out successfully'}, 200


