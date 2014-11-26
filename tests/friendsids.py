import tweepy
import os



def connect_to_API():
    """
    Create instance of tweepy API class with OAuth keys and tokens.
    """
    # initialize tweepy api object with auth, OAuth
    TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
    TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY, secure=True)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)
    api = tweepy.API(auth, cache=None)

    return api


def get_friends_ids(api, screen_name):
    """
    Request ids of all user's friends.

    Parameters:
    -----------
    A given user's screen name
    """

    try:
        print "User id for which we're requesting friends", screen_name
        friends_ids = api.friends_ids(screen_name = screen_name)

        print "get request friend ids"

        return friends_ids
    except tweepy.TweepError as e:
        print e

def main():
    api = connect_to_API()
    print api
    friends = get_friends_ids(api, "iamjohnoliver")
    print friends


if __name__=="__main__":
    main()
