"""
	API for getting tweets from Twitter hashtag feeds, scoring.
"""
import pickle
import tweepy
import dummyscore
import itertools
import os
import model



CURRENT_USER = ""
USER_SCORE = None

# tweepy api instance
api = None



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
	print "working!"
	while True:
		iterable1, iterable2 = itertools.tee(f_ids)
		f_ids, page = (itertools.islice(iterable1, page_size, None),
		        list(itertools.islice(iterable2, page_size)))
		if len(page) == 0:
		    break
		# yield is a generator keyword
		yield page



def connect_to_API():
	"""
	Create instance of tweepy API class with OAuth keys and tokens.
	"""
	global api
	# initialize tweepy api object with auth, OAuth
	TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
	TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
	TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
	TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')

	auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY, secure=True)
	auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)
	api = tweepy.API(auth, cache=None) #removed wait_on_rate_limit=True, wait_on_rate_limit_notify=True

	return api


def get_tweets_by_query(api, query, count):
	"""
	search for {count} tweets labeled by a particular hashtag {query}

	Parameters:
	----------
	Count: the number of tweets per page. Maximum is 100.

	For use in my function:
	include_entities

	Output:
	------
	JSON object containing a list of statuses ["statuses"]

	"""


	try:
		search_results = tweepy.Cursor(api.search, q=query, lang="en").items(count)


	except tweepy.TweepError as e:
		pass

	return search_results

def load_tweets(session, statuses, label):
	"""loads search results into database"""
	for status in statuses:
		tweet = model.Status()
		tweet.id = status["id"]
		# print "TWEET_ID", tweet.id
		tweet.user_id = status["user"]["id"]
		# print "USER", tweet.user_id
		tweet.text = status["text"]
		# print "TEXT", tweet.text
		tweet.label = label

		# this code for some reason would only print "retweeted_status" and did not create a tweet object
		# if status["retweeted_status"]:
		# 	tweet.retweeted_from = status["retweeted_status"]["user"]["id"]
		# print "RETWEETED", tweet.retweeted_from

		created_at = status["created_at"][:10] + status["created_at"][25:]
		created_at = datetime.strptime(created_at, "%a %b %d %Y")
		tweet.created_at = created_at

		print "TWEET TO ADD", tweet

		session.add(tweet)

	# session.commit()

def main(session):
	api = connect_to_API()
	tcot = get_tweets_by_query(api, "#tcot", 10)
	# load_tweets(session, tcot, "cons")


if __name__ == "__main__":
	s = model.connect()
	main(s)




