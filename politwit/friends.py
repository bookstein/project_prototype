# -*- coding: utf-8 -*-
"""
    API for getting friends and statuses from Twitter.

"""

import itertools

import tweepy


class User(object):

    # class variables
    central_user = None  # screen name of user who was searched
    user_id = None  # any user's numeric ID
    screen_name = None  # any user's Twitter handle
    num_followers = None  # number of followers, assigned in flask_server
    score = None  # score assigned in score_user method

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
        Assigns value to
        self.api,
        self.user_id,
        self.central_user (if provided)
        """
        self.api = api
        self.central_user = central_user
        self.user_id = user_id

    def get_friends_ids(self):
        """
        Request ids of all user's friends.

        Parameters:
        -----------
        A given user's screen name
        """

        try:
            friends_ids = self.api.friends_ids(screen_name=self.central_user)
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
            return friends

        except tweepy.TweepError as e:
            print e

    def get_timeline(self, count):
        """
        Get n number of tweets by passing in user id and number of statuses.

        Parameters:
        -----------
        User id for which to get tweets
        Number of tweets to get

        Output:
        -------
        An array of {count} lower-cased tweet texts, including retweets.
        If user has protected tweets, returns [].
        """
        timeline = []

        try:
            for tweet in tweepy.Cursor(self.api.user_timeline, id=self.user_id,
                                       include_rts=True).items(count):
                timeline.append(tweet.text.lower())
            return timeline

        except tweepy.TweepError as e:
            print e
            return []

    def score_user(self, timeline, vectorizer, classifier):
        """
        Score user by averaging classifier probabilities for their recent
        timeline.

        Paramters:
        ---------
        Timeline, a list of recent tweets.
        An unpickled classifier.

        Output:
        -------
        A score between 0 and 1, representing the average probability of user's
        tweets being political.

        """
        score = 0

        vector = vectorizer.transform(timeline)
        prediction = classifier.predict(vector)
        probs = classifier.predict_proba(vector)

        print prediction
        print zip(prediction, timeline)
        print len(probs)

        # prob.item(1) is the probability of political content
        for prob in probs:
            score += prob.item(1)

        average_score = score / len(probs)

        return average_score
