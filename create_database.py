import sqlite3

connection = sqlite3.connect('hoteldatabase.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS hotels (hotel_id text PRIMARY KEY,\
  city text, name text, stars real, night real)"

create_hotel = "INSERT INTO hotels VALUES('ibis', 'Santa Catarina', 'Hotel Ibis', 4, 125.32)"

cursor.execute(create_table)
cursor.execute(create_hotel)

connection.commit()
connection.close() 