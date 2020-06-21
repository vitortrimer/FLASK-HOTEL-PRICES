from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument('login', type=str, required=True, help="'login' is a required field.")
args.add_argument('password', type=str, required=True, help="'password' is a required field.")
args.add_argument('name')


class User(Resource):

  def get(self, user_id):
    user = UserModel.find_user(user_id)
    if user:
      return user.json()
    else:
      return {'message': 'User not found.'}, 400

  @jwt_required
  def delete(self, user_id):
    user = UserModel.find_user(user_id)
    if user:
      try:
        user.delete_user()
      except:
        return {'message': 'Oops! An error ocurred trying to delete user'}, 500
      return {"message": "User '{}' have been deleted.".format(user.name)}
    else:
      return {"message": "User '{}' not found.".format(user_id)}, 400


class UserSignup(Resource):

  def post(self):
    data = args.parse_args()

    if UserModel.find_by_login(data['login']):
      return {"message": "Username '{}' already exists".format(data['login'])}, 400
    else:
      user = UserModel(**data)
      try:
        user.save_user()
      except:
        return {'message': 'Oops! An error ocurred trying to signup'}, 500

      return {'message': 'User created successfully'}, 201

class UserSignin(Resource):

  @classmethod
  def post(cls):
    data = args.parse_args()
    user = UserModel.find_by_login(data['login'])

    if user and safe_str_cmp(user.password, data['password']):
      access_token = create_access_token(identity=user.user_id)
      return {'access_token': access_token}, 200
    else:
      return {'message': 'Incorrect username or password'}, 401

class UserSignout(Resource):

  @jwt_required
  def post(self):
    jwt_id = get_raw_jwt()['jti'] #JWT Token Identifier
    BLACKLIST.add(jwt_id)
    return {'message': 'You have successfully signed out'}