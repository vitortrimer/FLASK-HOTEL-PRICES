from sql_alchemy import database

class HotelModel(database.Model):
  __tablename__ = 'hotels'

  hotel_id = database.Column(database.String, primary_key=True)
  city = database.Column(database.String(128))
  name = database.Column(database.String(160))
  stars = database.Column(database.Float(precision=1))
  night = database.Column(database.Float(precision=2))

  def __init__(self, hotel_id, city, name, stars, night):
    self.hotel_id = hotel_id
    self.city = city
    self.name = name
    self.stars = stars
    self.night = night

  def json(self):
    return {
      'hotel_id': self.hotel_id,
      'city': self.city,
      'name': self.name,
      'stars': self.stars,
      'night': self.night
    }
  
  @classmethod
  def find_hotel(cls, hotel_id):
    hotel = cls.query.filter_by(hotel_id=hotel_id).first()
    if hotel:
      return hotel
    else:
      return None

  def save_hotel(self):
    database.session.add(self)
    database.session.commit()

  def update_hotel(self, city, name, stars, night):
    self.city = city
    self.name = name
    self.stars = stars
    self.night = night

  def delete_hotel(self):
    database.session.delete(self)
    database.session.commit()