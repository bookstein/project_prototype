"""
	API for getting friends and statuses from Twitter, scoring.
"""
import os
import pickle
import tweepy
import dummyscore
import itertools

class User(object):

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
	USER_SCORE = None

	# tweepy api instance
	api = None

	def __init__(self):
		"""
		Create instance of tweepy API class with OAuth keys and tokens.
		"""
		auth = tweepy.OAuthHandler(self.TWITTER_API_KEY, self.TWITTER_SECRET_KEY, secure=True)
		auth.set_access_token(self.TWITTER_ACCESS_TOKEN, self.TWITTER_SECRET_TOKEN)
		self.api = tweepy.API(auth, cache=None) #removed wait_on_rate_limit=True, wait_on_rate_limit_notify=True

	# def paginate(iterable, page_size):

	def get_friends_ids(self,user_id):
		"""returns list of integers (friends_ids) of people that user (uid) is following"""
		try:
			friends_ids = tweepy.Cursor(self.api.friends_ids, user_id = user_id).items()
			# print friends_ids
			return friends_ids
		except tweepy.TweepError as e:
			print e

	def lookup_friends(self,f_ids):
		# if len(ids) > 100:
		try:
			friends = self.api.lookup_users(f_ids)
			return friends
		except tweepy.TweepError as e:
			print e

		# use output of get_friend_ids
		# hydrate (create twitter user object)
		# pickle dictionary

	def paginate_friends(self, f_ids, page_size):
	    print "working!"
	    while True:
	        iterable1, iterable2 = itertools.tee(f_ids)
	        f_ids, page = (itertools.islice(iterable1, page_size, None),
	                list(itertools.islice(iterable2, page_size)))
	        if len(page) == 0:
	            break
	        # yield is a generator keyword
	        yield page

	def get_top_influencers(self):
		pass
		"""
		Using paginated friends
		"""
		# friends_count attribute
		# do this if user has more than 300 friends (180 friends w user auth)

	def get_timeline(self, uid, count):
		"""Get n number of tweets by passing in user id and number of statuses.
			If user has protected tweets, returns [] rather than break the program.
		"""
		try:
			feed = tweepy.Cursor(self.api.user_timeline, id=uid).items(count)
			return feed

		except tweepy.TweepError as e:
			print e.message[0]["error"]
			return []

		# try:
		# except:
		# get user's timeline
		# statuses/user_timeline
		# create Status object
		# pickle dictionary

	def score_user(self):
		score = dummyscore.score()
		return score

	def get_links(self):
		pass
		# get link url, cut to hostname, compare against database


	def on_error(self):
		pass
		# handle errors here

	def check_rate_limit(self):
		pass
		# check rate limit for a given resource instead of hardcoding


def main():
	pass
	# currentUser = User(currentId)
	# currentUser.get_friends()
	# currentUser.get_timeline()

if __name__ == "__main__":
	# __init__ returns copy of Friends class, including api instance
	user = User()
	main()


