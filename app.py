from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.hotel import Hotels, Hotel
from resources.user import User, UserSignup, UserSignin, UserSignout
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'AlotOfSecret'
app.config['JWT_BLACKLIST_ENABLED'] = True

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_database():
  database.create_all()

@jwt.token_in_blacklist_loader
def verify_blacklsit(token):
  return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def access_token_invalidated():
  return jsonify({'message': 'You need to signin to do this operation'}), 401

api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:hotel_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UserSignup, '/signup')
api.add_resource(UserSignin, '/signin')
api.add_resource(UserSignout, '/signout')

if __name__ == '__main__':
  from sql_alchemy import database
  database.init_app(app)
  app.run(debug=True)
