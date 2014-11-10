"""
	API for getting friends and statuses from Twitter, scoring.
"""

import pickle
import tweepy
import score

# initialize tweepy api object with auth, OAuth
TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')

# important variables
MAX_NUM_TWEETS = 100
MAX_NUM_FRIENDS = 300
TIME_TO_WAIT = 900/180 # 15 minutes divided into 180 requests
NUM_RETRIES = 2
RATE_LIMITED_RESOURCES =[("statuses", "/statuses/user_timeline")]

class User(Object):
	"""A user will be a node in the graph.
	Every user will be initialized with an id_str. Users who are friends of the central user will be initialized with that user's id_str.
	Other data: followers_count(influence), protected status (True/False), screen name, and statuses_count.

	Users whose tweets are protected will be thrown out unless user is logged in (login functionality is p2)"""
	pass
	# pass in user id to initialize user

	def get_friend_ids(self):
		pass
		# get friends ids
		# return friends_ids for hydrate_users
		try:
			# get ids
		except:
			# print exception/error

	def hydrate_users(self):
		pass
		# use output of get_friend_ids
		# hydrate (create twitter user object)
		# pickle dictionary

	def get_top_influencers(self):
		pass
		# friends_count attribute
		# do this if user has more than 300 friends (180 friends w user auth)

	def get_timeline(self):
		pass
		# get user's timeline
		# statuses/user_timeline
		# pickle dictionary

	def score_user(self):
		pass
		# score user by tweets
		# store (in DB???)

	def __init__(self, user_id, followed_by="self"):
		pass
		# initializes any user by user id.
		# followed_by (optional param) records the relationship of the User to the primary user account.
		# must designate a "current user"/central user at some point
		# user name, user id
		# get score

class Status(Object):
	pass
	"""
	Status initialized by id.
	Statuses will contain entities (expanded url, hashtags), id_str, retweeted status, text, and user id
	"""

	def __init__(self, id, user_id):
		# initialize tweet by tweet id??
		# get links
		# get score
		pass

	def get_links(self):
		pass
		# get link url, cut to hostname, compare against database

	def score_status(self):
		pass
		#score tweet based on links, possibly keywords/hashtags
		# use score module

def on_error():
	pass
	# handle errors here

def check_rate_limit():
	pass
	# check rate limit for a given resource instead of hardcoding

# currentUser = User(currentId)
# currentUser.get_friends()
# currentUser.get_timeline()



