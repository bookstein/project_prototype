import os
import json
import time
import cPickle as pickle

from flask import Flask, url_for, request, render_template, redirect, flash
import tweepy

from friends import User

app = Flask(__name__)
app.secret_key = 'politicaltwitter'


TIME_TO_WAIT = 3  # in seconds
NUM_RETRIES = 2  # number of retries Tweepy API object should make

PATH_TO_VECTORIZER = "politwit/vectorizer.pkl"
PATH_TO_CLASSIFIER = "politwit/classifierNB.pkl"

TEST_SET = ["bookstein", "ladygaga", "maddow", "glennbeck"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax/user", methods=["POST"])
def get_user():
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
    api = connect_to_API()

    with open(PATH_TO_CLASSIFIER, "rb") as f:
        classifier = pickle.load(f)

    with open(PATH_TO_VECTORIZER, "rb") as f:
        vectorizer = pickle.load(f)

    user = User(api, central_user=screen_name, user_id=screen_name)
    timeline = user.get_timeline(user.USER_ID, user.MAX_NUM_TWEETS)

    # initialize friend_scores object, which will pass friends and scores to d3
    friend_scores = {"name": user.USER_ID, "children": []}

    try:
        friends_ids = user.get_friends_ids(screen_name)

        friendlist = [user]

        for page in user.paginate_friends(friends_ids, 100):
            friends = process_friend_batch(user, page, api)
            friendlist.extend(friends)

        if len(friendlist) > user.MAX_NUM_FRIENDS:
            friendlist = get_top_influencers(friendlist, user.MAX_NUM_FRIENDS)

        for friend in friendlist:
            timeline = friend.get_timeline(friend.USER_ID,
                                           friend.MAX_NUM_TWEETS)
            friend.SCORE = friend.score(timeline, vectorizer, classifier)

            friend_scores["children"].append({"name": friend.SCREEN_NAME,
                                             "size": friend.NUM_FOLLOWERS,
                                             "score": friend.SCORE})

        json_scores = json.dumps(friend_scores)
        return json_scores

    except tweepy.TweepError as e:
        error_message = handle_error(e)
        flash(error_message)
        return redirect(url_for("index"))


@app.route("/demo/prefetched/<screen_name>")
def get_prefetched(screen_name):
    time.sleep(TIME_TO_WAIT)
    with open(screen_name + ".pkl") as f:
        scores = pickle.load(f)

    json_scores = json.dumps(scores)
    return json_scores


def process_friend_batch(user, page, api):
    """
    Create User object for each friend in batch of 100 (based on pagination)
    """
    batch = []
    friend_objs = user.lookup_friends(f_ids=page)
    for f in friend_objs:
        friend = User(api, central_user=user.CENTRAL_USER, user_id=f.id)
        friend.NUM_FOLLOWERS = f.followers_count
        friend.SCREEN_NAME = f.screen_name
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
                                 key=lambda x: x.NUM_FOLLOWERS,
                                 reverse=True)
    friendlist = sorted_by_influence[:count]

    return friendlist


def handle_error(e):
    if e.args[0][0]['code'] == "88":
        return "Rate limit exceeded: please wait a few minutes to retry."
    else:
        return "Error: We encountered an error while contacting Twitter: \n"
        + e.args[0][0]["message"]


def connect_to_API():
    """
    Create instance of tweepy API class with OAuth keys and tokens.
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
