from sql_alchemy import database

class UserModel(database.Model):
  __tablename__ = 'users'

  user_id = database.Column(database.Integer, primary_key=True)
  login = database.Column(database.String(40))
  password = database.Column(database.String(40))
  name = database.Column(database.String(120))

  def __init__(self, login, password, name):
    self.login = login
    self.password = password
    self.name = name
    
  def json(self):
    return {
      'user_id': self.user_id,
      'login': self.login,
      'name': self.name
    }

  @classmethod
  def find_user(cls, user_id):
    user = cls.query.filter_by(user_id=user_id).first()
    if user:
      return user
    else:
      return None

  @classmethod
  def find_by_login(cls, login):
    user = cls.query.filter_by(login=login).first()
    if user:
      return user
    else:
      return None

  def save_user(self):
    database.session.add(self)
    database.session.commit()

  def delete_user(self):
    database.session.delete(self)
    database.session.commit()
    