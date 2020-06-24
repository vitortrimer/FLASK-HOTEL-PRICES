from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(city=None, min_stars=0, max_stars=5, min_night=0, max_night=10000, limit=50, offset=0, **data):
  if city:
    return {
      'min_stars': min_stars,
      'max_stars': max_stars,
      'min_night': min_night,
      'max_night': max_night,
      'city': city,
      'limit': limit,
      'offset': offset
    }
  else:
    return {
      'min_stars': min_stars,
      'max_stars': max_stars,
      'min_night': min_night,
      'max_night': max_night,
      'limit': limit,
      'offset': offset
    }


path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('min_stars', type=float)
path_params.add_argument('max_stars', type=float)
path_params.add_argument('min_night', type=float)
path_params.add_argument('max_night', type=float)
path_params.add_argument('limit', type=int)
path_params.add_argument('offset', type=int)

class Hotels(Resource):
  def get(self):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    data = path_params.parse_args()
    valid_data = {key:data[key] for key in data if data[key] is not None}
    parameters = normalize_path_params(**valid_data)

    if not parameters.get('city'):
      query = "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?) \
      and (night >= ? and night <= ?) \
      LIMIT ? OFFSET ?"
      query_tuple = tuple([parameters[key] for key in parameters])
      result = cursor.execute(query, query_tuple)
    else:
      print([parameters[key] for key in parameters])
      query = "SELECT * FROM hotels WHERE (stars >= ? and stars <= ?) \
      and (night >= ? and night <= ?) \
      and city = ?\
      LIMIT ? OFFSET ?"
      query_tuple = tuple([parameters[key] for key in parameters])
      result = cursor.execute(query, query_tuple)

    hotels = []
    for line in result:
      hotels.append({
        'hotel_id': line[0],
        'city': line[1],
        'name': line[2],
        'stars': line[3],
        'night': line[4]
      })

    return {'hotels': hotels}

class Hotel(Resource):
  args = reqparse.RequestParser()
  args.add_argument('city')
  args.add_argument('name', type=str, required=True, help="'name' is a required field.")
  args.add_argument('stars')
  args.add_argument('night')

  def get(self, hotel_id):
    hotel = HotelModel.find_hotel(hotel_id)
    if hotel:
      return hotel.json()
    else:
      return {'message': 'Hotel not found.'}, 400

  @jwt_required
  def post(self, hotel_id):
    if HotelModel.find_hotel(hotel_id):
      return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400
    
    data = Hotel.args.parse_args()
    hotel = HotelModel(hotel_id, **data)
    try:
      hotel.save_hotel()
    except:
      return {'message': 'Oops! An error ocurred trying to saving hotel'}, 500
    return hotel.json()

  @jwt_required
  def put(self, hotel_id):
    data = Hotel.args.parse_args()
    found_hotel = HotelModel.find_hotel(hotel_id)

    if found_hotel:
      found_hotel.update_hotel(**data)
      try:
        found_hotel.save_hotel()
      except:
        return {'message': 'Oops! An error ocurred trying to edit hotel'}, 500
      return found_hotel.json(), 200

    hotel = HotelModel(hotel_id, **data)
    hotel.save_hotel()
    return hotel.json(), 201

  @jwt_required
  def delete(self, hotel_id):
    hotel = HotelModel.find_hotel(hotel_id)
    if hotel:
      try:
        hotel.delete_hotel()
      except:
        return {'message': 'Oops! An error ocurred trying to delete hotel'}, 500
      return {"message": "Hotel '{}' have been deleted.".format(hotel_id)}
    else:
      return {"message": "Hotel '{}' not found.".format(hotel_id)}, 400

