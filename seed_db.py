from os import path, makedirs
import friends
import json
from datetime import datetime
import model


def check_rate_limit_status(resource_family, resource):
	"""
	Returns initial number of allowed API calls, per Twitter rate limits, for a given resource family and resource.
	Example: to check statuses (tweets), use resource family "statuses", resource "/statuses/user_timeline"

	For other resources, see Twitter API docs: https://dev.twitter.com/rest/reference/get/application/rate_limit_status
	"""
	rate_info = twitter_user.api.rate_limit_status()['resources']
	initial_rate_limit = int(rate_info[resource_family][resource]["remaining"])
	return initial_rate_limit


def make_friends_list(username):
	FRIENDS = twitter_user.get_friends(username)
	return FRIENDS

def load_twitter_timeline(username, session, count):
	try:
		# establish API connection
		twitter_user = friends.User()

		statuses = twitter_user.get_timeline(username, count)
		# print "STATUSES", statuses # prints tweepy ItemIterator

		for status in statuses:
			status = status._json
			# print "STATUS", status
			tweet = model.Status()
			tweet.id = status["id"]
			# print "TWEET_ID", tweet.id
			tweet.user_id = status["user"]["id"]
			# print "USER", tweet.user_id
			tweet.text = status["text"]
			# print "TEXT", tweet.text

			# this code for some reason would only print "retweeted_status" and did not create a tweet object
			# if status["retweeted_status"]:
			# 	tweet.retweeted_from = status["retweeted_status"]["user"]["id"]
			# print "RETWEETED", tweet.retweeted_from

			created_at = status["created_at"][:10] + status["created_at"][25:]
			created_at = datetime.strptime(created_at, "%a %b %d %Y")
			tweet.created_at = created_at

			print "TWEET TO ADD", tweet

			session.add(tweet)

		session.commit()

	except Exception as e:
		print e



def main(session):
	TEST = ["bookstein"]
	USERS = ["maddow", "rushlimbaugh", "iamjohnoliver", "SenRandPaul"]
	COUNT = 100 # number of tweets to get per person
	TIME_TO_WAIT = 900 / 180

	for user in USERS:
		load_twitter_timeline(user, session, COUNT)

if __name__ == "__main__":
	s = model.connect()
	main(s)