"""
	API for getting friends and statuses from Twitter, scoring.
"""
import os
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

CURRENT_USER = ""

auth = None
api = None

def init_api():
	"""
	Create global tweepy API object with OAuth keys and tokens.
	Call this function from flask server
	"""
	global api
	auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY, secure=True)
	auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)
	api = tweepy.API(auth, cache=None) #removed wait_on_rate_limit=True, wait_on_rate_limit_notify=True
	return auth, api

# def paginate(iterable, page_size):

def get_friend_ids(user_id):
	try:
		friends_ids = tweepy.Cursor(api.friends_ids, user_id = user_id).pages()
		print friends_ids
		return friends_ids
	except tweepy.TweepError as e:
		print e

def hydrate_users(ids):
	# if len(ids) > 100:
	try:
		friends = api.lookup_users(ids)
		print friends
	except tweepy.TweepError as e:
		print e

	# use output of get_friend_ids
	# hydrate (create twitter user object)
	# pickle dictionary

def get_top_influencers(self):
	pass
	# friends_count attribute
	# do this if user has more than 300 friends (180 friends w user auth)

def get_timeline(self):
	pass
	# try:
	# except:
	# get user's timeline
	# statuses/user_timeline
	# create Status object
	# pickle dictionary

def score_user(self):
	pass
	# score user by tweets
	# store (in DB???)


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

def main():
	pass
	# currentUser = User(currentId)
	# currentUser.get_friends()
	# currentUser.get_timeline()

if __name__ == "__main__":
	main()


