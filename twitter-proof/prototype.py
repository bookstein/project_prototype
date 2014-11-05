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
	print tweet.text

user = api.get_user('twitter')
print user.screen_name