from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint #have these on same line?

ENGINE = create_engine("sqlite:///tweets.db", echo=False)
db_session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush = False))

Base = declarative_base()
Base.query = db_session.query_property()

### Code for creating the database - on command line
# python -i model.py
# engine = create_engine("sqlite:///tweets.db", echo=True)
# Base.metadata.create_all(engine)

#add single table
# engine = create_engine("sqlite:///tweets.db", echo=True)
# Base.metadata.tables["statuses"].create(bind=engine)

######################
# class declarations #
######################

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True) #same as twitter id?
	screen_name = Column(String(20), unique=True, nullable=False)
	num_followers = Column(Integer)
	num_friends = Column(Integer)
	score = Column(Integer, nullable=True)

class Status(Base):
	__tablename__ = "statuses"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	text = Column(String(140), nullable=False) # tweet can't be empty
	url = Column(String(140), nullable=True)
	retweeted_from = Column(Integer, nullable=True)
	created_at = Column(Date)
	label = Column(String(20), nullable=False)

	#creates "statuses" attribute of user
	user = relationship("User", backref = backref("statuses"), order_by=id)

	@classmethod
	def get_all_statuses(cls):
		"""
		Return all rows from statuses table.

		Parameter 'cls' references the Status class.
		"""
		statuses = cls.query.all()
		return statuses

	@classmethod
	def update_a_duplicate(cls):
		"""
		If a tweet is already in the database, update the existing tweet.
		"""
		pass

class Hashtag(Base):
	__tablename__ = "hashtags"

	id = Column(Integer, primary_key=True)
	tweet_id = Column(Integer, ForeignKey('statuses.id'), nullable=False)
	text = Column(String(60))

	# creates "hashtags" atribute of tweet
	status = relationship("Status", backref = backref("hashtags"))

class PoliticalHashtag(Base):
	__tablename__ = "hashtag_features"

	id = Column(Integer, primary_key=True)
	text = Column(String(60))
	score = Column(Integer, nullable=True)


def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///tweets.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


def main():
	pass

if __name__ == "__main__":
    main()
