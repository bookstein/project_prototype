import twitter
import os

TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')

# print TWITTER_SECRET_TOKEN
# print TWITTER_SECRET_KEY
# print TWITTER_ACCESS_TOKEN
# print TWITTER_API_KEY

auth = twitter.oauth.OAuth(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN, TWITTER_API_KEY, TWITTER_SECRET_KEY)
twitter_api = twitter.Twitter(auth=auth)

# testing out search API
# url = "https://api.twitter.com/1.1/search/tweets.json?q=voter&src=typd"


q = 'voter' # query
count = 5
results = twitter_api.search.tweets(q=q, count=count)
statuses = results['statuses']
print statuses

for _ in range(count):
	# print statuses
	try:
		next_results = results['search_metadata']['next_results']

	# when no more results exist
	except KeyError, e:
		break

# print statuses # NOTE: a count of 100 took a second to process.