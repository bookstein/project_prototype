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

def get_feed():
	# returns 20 most recent statuses from authenticated user feed
	public_tweets = api.home_timeline()
	for tweet in public_tweets:
		pass

def get_timeline(uid):
	#Returns the 20 most recent statuses posted from the authenticating user
	tweets = api.user_timeline(uid)
	return tweets

def get_user_by_id(uid):
	# get_user can take screen_name or user_id
	# id is the generic case (could be either type)
	user = api.get_user(uid)
	return user

def get_friends(uid):
	# returns list of integers (ids) of people user is following
	friends_ids = api.friends_ids(uid)
	return friends_ids

def get_links(tweets):
	url = tweets[0]["expanded_url"]
	return url

def main():
	friends = get_friends("bookstein")
	friend_id = get_user_by_id(friends[0]).id
	print friend_id
	tweets = get_timeline(friend_id)
	print tweets

if __name__ == "__main__":
	main()




