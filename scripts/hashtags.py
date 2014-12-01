"""
    Script for getting and pickling co-occurring hashtags based on seed hashtags.
"""
import os
import pickle

import tweepy

import politwit.model as model

POLITICAL_SEED_HASHTAGS = ["p2", "tcot"]
NONPOLITICAL_SEED_HASHTAGS = ["ff", "tbt", "nowplaying", "gameinsight","love", "win", "ipad"]
EXCLUDE_HASHTAGS =  "-#RT -#rt -#TeamFollowBack -#followback"
TWEETS_TO_GET = 100

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
    Search for {max_tweets} tweets labeled by a particular hashtag {query}

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
            new_tweets = api.search(q=query, lang="en", count=count, include_entities=True, max_id=str(max_id - 1))
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
            # depending on TweepError.code --> retry or wait
            # for now give up on an error
            break
    return searched_tweets



def load_hashtags(statuses, label, hashtags_seen):
    """
    Iterate through searched tweets, pickle dictionary of co-occurring hashtags.

    Parameters:
    ----------
    Statuses from Twitter API query
    Label
    Dictionary of hashtags and counts to return to main() scope

    Output:
    ------
    Dictionary of hashtag, count pairs from given list of statuses.
    """

    for status in statuses:

        hashtags_from_tw = status["entities"]['hashtags']
        for hashtag_obj in hashtags_from_tw:
            hashtag = hashtag_obj["text"].lower()
            hashtags_seen[hashtag] = hashtags_seen.get(hashtag, 0) + 1

    return hashtags_seen


def main():
    print "running main"
    api = connect_to_API()

    # hashtags_seen = {}

    # for hashtag in POLITICAL_SEED_HASHTAGS:
    #     htg_tweets = get_tweets_by_query(api, hashtag, TWEETS_TO_GET/10)
    #     load_hashtags(htg_tweets, "p", hashtags_seen)

    # with open("p_hashtags.pkl", "w+") as f:
    #     pickle.dump(hashtags_seen, f)

    hashtags_seen = {}

    for hashtag in NONPOLITICAL_SEED_HASHTAGS:
        htg_tweets = get_tweets_by_query(api, ("#" + hashtag + " -#p2 -#tcot " + EXCLUDE_HASHTAGS), TWEETS_TO_GET)
        load_hashtags(htg_tweets, "np", hashtags_seen)

    with open("np_hashtags.pkl", "w+") as f:
        pickle.dump(hashtags_seen, f)

if __name__ == "__main__":
    main()




