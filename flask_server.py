import os
import json
import time
import cPickle as pickle

from flask import Flask, url_for, request, render_template, redirect, flash
import tweepy

from politwit.friends import User

app = Flask(__name__)
app.secret_key = 'politicaltwitter'


# important variables
TIME_TO_WAIT = 3  # in seconds
NUM_RETRIES = 2  # number of retries Tweepy API object should make
MAX_NUM_TWEETS = 20
MAX_NUM_FRIENDS = 50

PATH_TO_VECTORIZER = "politwit/vectorizer.pkl"
PATH_TO_CLASSIFIER = "politwit/classifierNB.pkl"

TEST_SET = ["bookstein", "ladygaga", "maddow", "glennbeck"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax/user", methods=["POST"])
def get_user():
    """
    Get username from AJAX POST request.
    Request user from Twitter API, as a way to quickly verify that the
    screen name exists.

    If the screen name exists, redirect to display_friends.
    """
    api = connect_to_API()

    screen_name = request.json["screen_name"]

    if screen_name in TEST_SET:
        return redirect(url_for("get_prefetched", screen_name=screen_name))

    try:
        # check to make sure this user exists before proceeding
        user = api.get_user(screen_name=screen_name, include_entities=False)
        if user.id_str:
            return redirect(url_for("display_friends",
                            screen_name=screen_name))
        else:
            flash("Error: Twitter couldn't find that username.")
            return redirect(url_for("index"))

    except tweepy.TweepError as e:
        error_message = handle_error(e)
        flash(error_message)
        return redirect(url_for("index"))


@app.route("/get/display/<screen_name>")
def display_friends(screen_name):
    """
    For a given user, select top 50 most influential friends (by number of
    followers) and send JSON back to the front end for visualization.

    Parameters:
    ----------
    A user's screen name.

    Output:
    ------
    JSON of friends' screen names, number of followers, and scores.

    TODO: Refactor this route into 2 separate routes, in order to be able to
    update the front end more frequently.
    TODO: Add the searched user to friendlist, to be displayed in d3.

    """
    api = connect_to_API()
    friendlist = []
    user = User(api, central_user=screen_name, user_id=screen_name)

    with open(PATH_TO_CLASSIFIER, "rb") as f:
        classifier = pickle.load(f)

    with open(PATH_TO_VECTORIZER, "rb") as f:
        vectorizer = pickle.load(f)

    # initialize friend_scores object, which stores
        # friends, followers and scores as objects inside "children" list
    friend_scores = {"name": user.user_id, "children": []}

    try:
        friends_ids = user.get_friends_ids()

        for page in user.paginate_friends(friends_ids, 100):
            friends = process_friend_batch(user, page, api)
            friendlist.extend(friends)

        if len(friendlist) > MAX_NUM_FRIENDS:
            friendlist = get_top_influencers(friendlist, MAX_NUM_FRIENDS)

        for friend in friendlist:
            timeline = friend.get_timeline(MAX_NUM_TWEETS)
            friend.score = friend.score_user(timeline, vectorizer, classifier)

            friend_scores["children"].append({"name": friend.screen_name,
                                             "size": friend.num_followers,
                                             "score": friend.score})

        json_scores = json.dumps(friend_scores)
        return json_scores

    except tweepy.TweepError as e:
        error_message = handle_error(e)
        flash(error_message)
        return redirect(url_for("index"))


@app.route("/demo/prefetched/<screen_name>")
def get_prefetched(screen_name):
    """
    Some users have so many Twitter friends that performance is significantly
    affected. A few pre-chosen users are redirected here immediately.
    Unpickle user's already-created JSON of friends, followers and scores.

    Parameters:
    ----------
    Screen name, as specified in "test set" variable

    Output:
    -------
    JSONified python dictionary of scores, ready to be visualized.

    """
    time.sleep(TIME_TO_WAIT)
    with open(screen_name + ".pkl") as f:
        scores = pickle.load(f)

    json_scores = json.dumps(scores)
    return json_scores


def process_friend_batch(user, page, api):
    """
    Create User object for each friend in batches of 100.
    Return batch as list of friend objects.

    Parameters:
    -----------
    User object
    A page of 100 friend ids (Twitter rate limit for user/lookup is 100 ids)
    API object

    Output:
    -------
    A list of 100 friend objects.

    """
    batch = []
    friend_objs = user.lookup_friends(f_ids=page)
    for f in friend_objs:
        friend = User(api, central_user=user.central_user, user_id=f.id)
        friend.num_followers = f.followers_count
        friend.screen_name = f.screen_name
        batch.append(friend)
    return batch


def get_top_influencers(friendlist, count):
    """
    Get top influencers from user friends, as measured by # of followers.

    After requesting paginated friends, check "followers_count" attribute of
    each friend.

    Note:
    -----
    Run this function only if user has more than {count} friends.
    Currently, Twitter limits user timeline requests to 300
    (application auth) or 180 requests (user auth).

    Parameters:
    ----------
    List of all friend objects.
    Number of top influencers to output.

    Output:
    -------
    List of {count} most influential friends

    """

    sorted_by_influence = sorted(friendlist,
                                 key=lambda x: x.num_followers,
                                 reverse=True)
    friendlist = sorted_by_influence[:count]

    return friendlist


def handle_error(e):
    """
    Return a string message depending on Tweepy error code.

    Parameters:
    -----------
    tweepy.TweepError

    Output:
    -------
    String error message

    """
    if e.args[0][0]['code'] == "88":
        return "Rate limit exceeded: please wait a few minutes to retry."
    else:
        return "Error: We encountered an error while contacting Twitter: \n"
        + e.args[0][0]["message"]


def check_rate_limit(api):
    """
    Check Twitter API rate limit status for "users" and "statuses" (tweets)
    requests
    Print number of requests remaining per time period.
    """
    limits = api.rate_limit_status()
    tweets = limits["resources"]["statuses"]
    users = limits["resources"]["users"]
    for resource in tweets.keys():
        if tweets[resource]["remaining"] == 0:
            print "EXPIRED:", resource
        else:
            print resource, ":", tweets[resource]["remaining"], "\n"
    for resource in users.keys():
        if users[resource]["remaining"] == 0:
            print "EXPIRED:", resource
        else:
            print resource, ":", users[resource]["remaining"], "\n"


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
    api = tweepy.API(auth, cache=None, retry_count=NUM_RETRIES)

    return api

if __name__ == "__main__":
    app.run(debug=True)
