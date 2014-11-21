from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint #have these on same line?

ENGINE = create_engine("sqlite:///data.db", echo=False)
db_session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush = False))

Base = declarative_base()
Base.query = db_session.query_property()

######################
# class declarations #
######################

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True) #same as twitter id?
	screen_name = Column(String(20), unique=True, nullable=False)
	score = Column(Integer)
	location = Column(String(60))

class Relationship(Base):
	__tablename__ = "relationships"

	id = Column(Integer, primary_key=True) # relationship id
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	friend_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	follow_back = Column(Boolean)

class Status(Base):
	__tablename__ = "statuses"

	id = Column(Integer, primary_key=True) #same as twitter status id?
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	text = Column(String(140), nullable=False) # tweet can't be empty
	url = Column(String(140))

	#creates "statuses" attribute of user
	user = relationship("User", backref = backref("statuses"), order_by=id)

def main():
	pass

if __name__ == "__main__":
    main()
