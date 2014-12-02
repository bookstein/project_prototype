# -*- coding: utf-8 -*-
"""
    API for getting friends and statuses from Twitter.

"""

import itertools

import tweepy


class User(object):

    # class variables
    central_user = None
    user_id = None
    screen_name = None
    num_followers = None
    score = None

    def __init__(self, api, central_user=None, user_id=None):
        """
        Initialize new user object.

        Parameters:
        ----------
        ID for the user whose friends will be analyzed.
        Tweepy API object
        User Id (Screen name or ID number) of friend

        Output:
        ------
        Assigns value to self.api, self.USER_ID
        """
        self.api = api
        self.CENTRAL_USER = central_user
        self.USER_ID = user_id

    def get_friends_ids(self, screen_name):
        """
        Request ids of all user's friends.

        Parameters:
        -----------
        A given user's screen name
        """

        try:
            # IF USING MEMCACHE: wrap it around API calls
            # key = derive_key(obj)
            # obj = mc.get(key)
            #if not obj:
                #obj = backend_api.get(...) <-- friends_ids = api.get(...)
                #mc.set(key, obj)
            print "User id for which we're requesting friends", screen_name
            friends_ids = self.api.friends_ids(screen_name=screen_name)

            # logging.info("Api request: ", friends_ids,
                # "\n")
            print "get request friend ids"

            # for friend in friends_ids:
            #   print friend

            return friends_ids
        except tweepy.TweepError as e:
            print e

    def paginate_friends(self, f_ids, page_size):
        """
        Paginate friend ids.

        Parameters:
        ----------
        List of friend ids (list of integers)
        Page size (number of friend ids to include per page)

        Note:
        ----
        Page_size maximum value is 100 due to Twitter API limits for
        users/lookup

        Output:
        -------
        Lists of {page_size} number of friend ids, to pass to lookup_friends

        """
        while True:
            iterable1, iterable2 = itertools.tee(f_ids)
            f_ids, page = (itertools.islice(iterable1, page_size, None),
                           list(itertools.islice(iterable2, page_size)))
            if len(page) == 0:
                break
            # yield is a generator keyword
            print "PRINTING PAGE ", page
            yield page

    def lookup_friends(self, f_ids):
        """
        Hydrates friend ids into complete user objects.

        Note:
        -----
        Takes only up to 100 ids per request.

        Parameters:
        ----------
        Page of friends_ids, the output of paginate_friends

        Output:
        ------
        List of user objects for the corresponding ids.

        """
        try:

            friends = self.api.lookup_users(f_ids)
            # logging.info("Lookup users: ", friends, "\n")
            print "get request friends hydrated"

            # for friend in friends:
            #   print friend

            return friends
        except tweepy.TweepError as e:
            print e

        # use output of get_friends_ids
        # hydrate (create twitter user object)
        # pickle dictionary

    def get_timeline(self, uid, count):
        """
        Get n number of tweets by passing in user id and number of statuses.
        If user has protected tweets, returns [].

        Parameters:
        -----------
        User id for which to get tweets
        Number of tweets to get

        Output:
        -------
        An array of {count} lower-cased tweet texts, including retweets.
        """
        timeline = []

        try:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=uid,
                                       include_rts=True).items(count):
                timeline.append(tweet.text.lower())

            print "get request timeline"
            return timeline

        except tweepy.TweepError as e:
            print e
            return []

        # try:
        # except:
        # get user's timeline
        # statuses/user_timeline
        # create Status object
        # pickle dictionary

    def count_hashtags(self, timeline):
        """
        Store hashtags from a given timeline in a dictionary.

        Parameters:
        ----------
        Takes a tweepy cursor object corresponding to a user's timeline.

        Output:
        ------
        A dictionary of all hashtags (lowercased) used, with count as value.

        """
        hashtags_dict = {}

        for tweet in timeline:
            # print "processing tweet"
            hashtags_in_tweet = tweet.entities["hashtags"]
            for hashtag_obj in hashtags_in_tweet:
                # print "counting hashtags"
                hashtag = hashtag_obj["text"].lower()
                hashtags_dict[hashtag] = hashtags_dict.get(hashtag, 0) + 1
        return hashtags_dict

    def score(self, timeline, vectorizer, classifier):
        """
        Score user by averaging classifier probabilities for timeline.

        Paramters:
        ---------
        Timeline, a list of recent tweets.
        An unpickled classifier.

        Output:
        -------
        A score between 0 and 1, representing the average probability of
        tweets being political.

        """
        print "Scoring"
        score = 0

        vector = vectorizer.transform(timeline)
        prediction = classifier.predict(vector)
        probs = classifier.predict_proba(vector)

        print prediction
        print zip(prediction, timeline)
        print len(probs)

        # prob.item(1) is the probability of political
        # ndarray ordered lexigraphically (np before p)
        for prob in probs:
            score += prob.item(1)

        average_score = score / len(probs)
        print average_score

        return average_score


def check_rate_limit(api):
    """
    Check Twitter API rate limit status for "statuses" (timeline) requests
    Print number of requests remaining per time period
    """
    limits = api.rate_limit_status()
    stats = limits["resources"]["statuses"]
    for resource in stats.keys():
        if stats[resource]["remaining"] == 0:
            print "EXPIRED:", resource

        else:
            print resource, ":", stats[resource]["remaining"], "\n"
