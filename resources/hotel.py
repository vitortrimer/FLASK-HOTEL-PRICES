from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hotels(Resource):
  def get(self):
    return {'hotels': [hotel.json() for hotel in HotelModel.query.all()]}

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
