import tweepy
import os

TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')

# print TWITTER_SECRET_TOKEN
# print TWITTER_SECRET_KEY
# print TWITTER_ACCESS_TOKEN
# print TWITTER_API_KEY

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)

api = tweepy.API(auth)

public_tweets = api.home_timeline() # returns 20 most recent statuses, equivalent to timeline/home
for tweet in public_tweets:
	# print tweet.text
	pass

# get_user can take screen_name or user_id
# id is the generic case (could be either type)
uid = "bookstein"
user = api.get_user(uid)

# returns list of integers (ids) of people user is following
friends_ids = api.friends_ids(uid, cursor = -1)
for friend_id in friends_ids:
	print friend_id