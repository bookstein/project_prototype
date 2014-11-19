"""
	API for getting tweets from Twitter hashtag feeds, scoring.
"""
import pickle
import tweepy
import dummyscore
import itertools
import os



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
	""" search for {count} tweets labeled by a particular hashtag {query} """
	search_results = api.search(q=query, count=count, lang="en")

	print search_results

	for _ in range(5):
		print "Length of statuses", len(search_results)
		try:
			# next_results = search_results['search_metadata']['next_results']
			pass
		except KeyError, e: # No more results when next_results doesn't exist
			break


def main():
	api = connect_to_API()
	get_tweets_by_query(api, "#tcot", 10)


if __name__ == "__main__":
	main()




