from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, orm
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://postgres:example@localhost:5432/ap_lab')
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

class Location(Base):
   __tablename__ = "locations"
   id = Column(Integer, primary_key=True)

   name = Column(String)

class User(Base):
   __tablename__ = "users"
   id = Column(Integer, primary_key=True)

   first_name = Column(String)
   last_name = Column(String)
   password = Column(String)
   user_name = Column(String)
   location_id = Column(Integer, ForeignKey(Location.id))
   location = orm.relationship(Location, backref = "users", lazy = "joined")

class Ad(Base):
   __tablename__ = "advertisements"
   id = Column(Integer, primary_key=True)

   name = Column(String)
   status = Column(String)
   user_id = Column(Integer, ForeignKey(User.id))
   user = orm.relationship(User, backref = "advertisements", lazy = "joined")

   
