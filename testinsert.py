from modules import Session, User, Ad, Location
session = Session()

location = Location(name = "lviv")
user = User(first_name = "Marta", last_name = "Tymchyshyn", password = "qwerty", user_name = "qwerty", location_id = 1)
user1 = User(first_name = "qwndkj", last_name = "Tymchyshyn", password = "qwerty", user_name = "qwerty", location_id = 1)
ad = Ad(name = "qwerty", status = "posted", user_id = 1)
session.add(location)
session.add(user)
session.add(user1)
session.add(ad)
session.commit()