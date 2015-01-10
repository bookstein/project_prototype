import time
import os

import tweepy

from politwit.friends import User


def connect_to_API():
    """
    Return instance of tweepy API class, using OAuth keys and tokens stored as
    environmental variables.
    """
    # initialize tweepy api object with auth, OAuth
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_SECRET_KEY = os.environ.get('TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_SECRET_TOKEN = os.environ.get('TWITTER_SECRET_TOKEN')

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY,
                               secure=True)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)
    api = tweepy.API(auth, cache=None, retry_count=2)

    return api

api = connect_to_API()
user = User(api, "bookstein", "bookstein")

# get timeline
t0 = time.time()
timeline = user.get_timeline(20)
t1 = time.time()
print "TIME TO GET TIMELINE: ", t1 - t0

# get friends
t0 = time.time()
friends_ids = user.get_friends_ids()
t1 = time.time()
print "TIME TO GET FRIENDS:", t1 - t0

# paginate and lookup friends
t0 = time.time()
all_friends = []
for page in user.paginate_friends(friends_ids, 100):
        friend_objs = user.lookup_friends(page)
        for f in friend_objs:
            friend = User(api, user_id=f.id, central_user=user.central_user)
            friend.num_followers = f.followers_count
            friend.screen_name = f.screen_name
            all_friends.append(friend)
t1 = time.time()
print "TIME TO PAGINATE AND LOOKUP FRIENDS", t1 - t0

print all_friends

# get timelines for friends


