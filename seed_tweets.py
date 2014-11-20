"""
	API for getting tweets from Twitter hashtag feeds, scoring.
"""
import pickle
import tweepy
import dummyscore
import itertools
import os
import model
from datetime import datetime
from sqlalchemy.exc import IntegrityError


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


def get_tweets_by_query(api, query, max_tweets):
	"""
	search for {max_tweets} tweets labeled by a particular hashtag {query}

	Parameters:
	----------
	Api: the Tweepy API instance.
	Query: hashtag to search for, as a string, prefixed by "#"
	Max_tweets: the total number of tweets requested.

	Output:
	------
	List of JSON statuses

	Note:
	----
	Per 15 minutes, app can make 450 requests.
	Number of tweets per page defaults to 15. "Count" maximum is 100.

	"""
	searched_tweets = []

	max_id = -1

	while len(searched_tweets) < max_tweets:
	    count = max_tweets - len(searched_tweets)
	    try:
	        new_tweets = api.search(q=query, count=count, include_entities=True,
	         max_id=str(max_id - 1))
	        if not new_tweets:
	            break

	        for tweet in new_tweets:
	        	tweet = tweet._json
	        	searched_tweets.append(tweet)

	        max_id = new_tweets[-1].id
	        since_id = new_tweets[0].id

	        print "max_id:", max_id
	        print "since_id", since_id

	    except tweepy.TweepError as e:
	        # depending on TweepError.code, one may want to retry or wait
        	# to keep things simple, we will give up on an error
        	break
	return searched_tweets

def load_tweets(session, statuses, label):
	"""loads search results into database"""
	for status in statuses:
		tweet = model.Status()
		tweet.tweet_id = status["id"]
		# print "TWEET_ID", tweet.id
		tweet.user_id = status["user"]["id"]
		# print "USER", tweet.user_id
		tweet.text = status["text"]
		# print "TEXT", tweet.text
		tweet.label = label
		created_at = status["created_at"][:10] + status["created_at"][25:]
		created_at = datetime.strptime(created_at, "%a %b %d %Y")
		tweet.created_at = created_at

		print "TWEET TO ADD", tweet

		session.add(tweet)


def main(session):
	api = connect_to_API()
	tcot = get_tweets_by_query(api, "#tcot -#p2", 3000)
	p2 = get_tweets_by_query(api, "#p2 -#tcot", 3000)
	try:
		load_tweets(session, tcot, "cons")
		load_tweets(session, p2, "libs")
		session.commit()
	except IntegrityError as e:
		session.rollback()
	finally:
		session.close()

if __name__ == "__main__":
	s = model.connect()
	main(s)




