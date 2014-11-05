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

def get_timeline():
	public_tweets = api.home_timeline() # returns 20 most recent statuses, equivalent to timeline/home
	for tweet in public_tweets:
		# print tweet.text
		pass

def get_user_by_id(uid):
	# get_user can take screen_name or user_id
	# id is the generic case (could be either type)
	user = api.get_user(uid)
	return user

def get_friends(uid):
	# returns list of integers (ids) of people user is following
	friends_ids = api.friends_ids(uid)
	return friends_ids

def main():
	friends = get_friends("bookstein")
	print friends
	print get_user_by_id(friends[0]).screen_name

if __name__ == "__main__":
	main()




