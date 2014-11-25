"""
	API for getting friends and statuses from Twitter, scoring.
"""

import itertools
import os
import logging

import tweepy

import politwit.simplescore as simplescore

# logging.basicConfig(filename='api_requests.log',level=logging.DEBUG)

class User(object):

	# important variables
	MAX_NUM_TWEETS = 20
	MAX_NUM_FRIENDS = 50

	CENTRAL_USER = None
	USER_ID = None
	SCREEN_NAME = None
	NUM_FOLLOWERS = None
	SCORE = None

	# tweepy api instance
	api = None

	def __init__(self, api, central_user=None, user_id=None):
		"""
		Initialize new user object.

		Parameters:
		----------
		ID for the user whose friends will be analyzed.
		Tweepy API object
		User Id (Screen name or ID number) of friend

		Output:
		------
		Assigns value to self.api, self.USER_ID
		"""
		self.api = api
		self.CENTRAL_USER = central_user
		self.USER_ID = user_id

	def get_friends_ids(self, user_id):
		"""
		Request ids of all user's friends.

		Parameters:
		-----------
		A given user's id (screen name or id)
		"""

		try:
			# IF USING MEMCACHE: wrap it around API calls
			# key = derive_key(obj)
   			# obj = mc.get(key)
   			#if not obj:
   				#obj = backend_api.get(...) <-- friends_ids = api.get(...)
   				#mc.set(key, obj)
			friends_ids = tweepy.Cursor(self.api.friends_ids, user_id = user_id).items()

			# logging.info("Api request: ", friends_ids,
				# "\n")
			print "get request friend ids"
			return friends_ids
		except tweepy.TweepError as e:
			print e

	def paginate_friends(self, f_ids, page_size):
		"""
		Paginate friend ids.

		Parameters:
		----------
		List of friend ids (list of integers)
		Page size (number of friend ids to include per page)

		Note:
		----
		Page_size maximum value is 100 due to Twitter API limits for users/lookup

		Output:
		-------
		Lists of {page_size} number of friend ids, to pass to lookup_friends

		"""
		while True:
			iterable1, iterable2 = itertools.tee(f_ids)
			f_ids, page = (itertools.islice(iterable1, page_size, None),
			        list(itertools.islice(iterable2, page_size)))
			if len(page) == 0:
			    break
			# yield is a generator keyword
			print "PRINTING PAGE ", page
			yield page

	def lookup_friends(self, f_ids):
		"""
		Hydrates friend ids into complete user objects.

		Note:
		-----
		Takes only up to 100 ids per request.

		Parameters:
		----------
		Page of friends_ids, the output of paginate_friends

		Output:
		------
		List of user objects for the corresponding ids.

		"""
		try:

			friends = self.api.lookup_users(f_ids)
			# logging.info("Lookup users: ", friends, "\n")
			print "get request friends hydrated"
			return friends
		except tweepy.TweepError as e:
			print e

		# use output of get_friends_ids
		# hydrate (create twitter user object)
		# pickle dictionary

	def get_timeline(self, uid, count):
		"""Get n number of tweets by passing in user id and number of statuses.
			If user has protected tweets, returns [] rather than break the program.
		"""
		try:
			feed = tweepy.Cursor(self.api.user_timeline, id=uid).items(count)
			# logging.info("\n\n\n", "Get timeline: ", feed, "\n\n\n")
			print "get request timeline"
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

	def count_hashtags(self, timeline):
		"""
		Store hashtags from a given timeline in a dictionary.

		Parameters:
		----------
		Takes a tweepy cursor object corresponding to a user's timeline.

		Output:
		------
		A dictionary of all hashtags (lowercased) used and number of times used.

		"""
		hashtags_dict = {}

		for tweet in timeline:
			print "processing tweet"
			hashtags_in_tweet = tweet.entities["hashtags"]
			for hashtag_obj in hashtags_in_tweet:
				print "counting hashtags"
				hashtag = hashtag_obj["text"].lower()
				hashtags_dict[hashtag] = hashtags_dict.get(hashtag, 0) + 1
		return hashtags_dict


	def score(self, hashtags_dict):
		"""
		Score user based on number of politically-relevant hashtags.

		Paramters:
		---------
		Dictionary of hashtags and their counts found in recent timeline,
		created in count_hashtags() function.

		Output:
		-------
		A score between 0 and 1, representing the percentage of political
		hashtags out of all hashtags used.

		"""
		score = simplescore.Score(hashtags_dict)
		print "Scoring"
		self.SCORE = score.score

	def get_links(self):
		pass
		# get link url, cut to hostname, compare against database


def connect_to_API():
	"""
	Create instance of tweepy API class with OAuth keys and tokens.
	"""
	# initialize tweepy api object with auth, OAuth
	TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
	TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
	TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
	TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')

	auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY, secure=True)
	auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)
	api = tweepy.API(auth, cache=None) #removed wait_on_rate_limit=True, wait_on_rate_limit_notify=True
	return api

def main():
	pass

if __name__ == "__main__":
	# __init__ returns copy of Friends class, including api instance
	api = connect_to_API()
	# user = User(user_id="bookstein", api=api)



