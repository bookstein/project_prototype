import os
import logging
import time#, threading
import json
import datetime

from flask import Flask, url_for, request, render_template, redirect, flash
import tweepy

from friends import User
import politwit.model as model

app = Flask(__name__)


TIME_TO_WAIT = 900/180 # 15 minutes divided into 180 requests
NUM_RETRIES = 2
RATE_LIMITED_RESOURCES =[("statuses", "/statuses/user_timeline")]

# logging.basicConfig(filename='rate_limits.log',level=logging.DEBUG)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/ajax/user", methods=["POST"])
def get_user():
	api = connect_to_API()
	print check_rate_limit(api)

	screen_name = request.json["screen_name"]
	print "SCREEN NAME FROM JSON: ", screen_name

	if screen_name == "bookstein":
		return redirect("/ajax/testing")

	try:
		# check to make sure this user exists before proceeding
		user = api.get_user(screen_name=screen_name, include_entities=False)
		if user.id_str:
			return redirect(url_for("display_friends", screen_name=screen_name))
		else:
			return redirect(url_for("index")) #add flash message


	except tweepy.TweepError as e:
		print "ERROR GETTING USER ", e
		return redirect(url_for("index")) # add Flash messages


@app.route("/get/display/<screen_name>")
def display_friends(screen_name):
	api = connect_to_API()

	user = User(api, central_user=screen_name, user_id=screen_name)

	timeline = user.get_timeline(user.USER_ID, user.MAX_NUM_TWEETS)

	political_hashtags_dict = model.Hashtag.get_all_political_hashtags()

	try:
		friends_ids = user.get_friends_ids(screen_name)

		friendlist = [user]

		for page in user.paginate_friends(friends_ids, 100):
			friends = process_friend_batch(user, page, api)
			friendlist.extend(friends)

		if len(friendlist) > user.MAX_NUM_FRIENDS:
			print "ORIGINAL LEN", len(friendlist)
			friendlist = get_top_influencers(friendlist, user.MAX_NUM_FRIENDS)
			print "NEW LEN", len(friendlist)

	except tweepy.TweepError as e:
		print "ERROR!!!!!", e

	# initialized friend_scores object with root, children
	friend_scores = {"name": user.USER_ID, "children": []}

	try:
		for friend in friendlist:
			timeline = friend.get_timeline(friend.USER_ID, friend.MAX_NUM_TWEETS)
			print check_rate_limit(api)
			hashtag_count = friend.count_hashtags(timeline)
			friend.SCORE = friend.score(hashtag_count, political_hashtags_dict)

			friend_scores["children"].append({"name": friend.SCREEN_NAME, "size": friend.NUM_FOLLOWERS, "score": friend.SCORE})

	except tweepy.TweepError as e:
		print "ERROR!!!!!", e
		# logging.warning("ERROR: \n", check_rate_limit(api))

	if len(friend_scores) > 0:
		print "FRIEND SCORES", friend_scores
		json_scores = json.dumps(friend_scores)
		return json_scores

	else:
		return redirect("/")#, add flash --> errormessage="Unable to get friends")

@app.route("/ajax/tweets", methods=["GET", "POST"])
def get_latest_tweets():
	# user = User(api, user_id=screen_name)
	# tweets = user.get_timeline(user.USER_ID, 5)
	screen_name = request.json["screen_name"]
	print "SCREEN NAME FOR TWEETS", screen_name

	with open("cannedtweets.txt") as f:
		tweets = f.read()
		json_tweets = json.dumps(tweets)
		return json_tweets

@app.route("/ajax/testing")
def test_results():
	return json.dumps({'name': "bookstein", 'children': [{'score': 1.0, 'name': 'nytimes', 'size': 14133319}, {'score': 0, 'name': 'DalaiLama', 'size': 9821751}, {'score': 0.2222222222222222, 'name': 'BBCWorld', 'size': 8031573}, {'score': 0.0, 'name': 'nprnews', 'size': 3054552}, {'score': 1.0, 'name': 'maddow', 'size': 3042640}, {'score': 0.0, 'name': 'TheDailyShow', 'size': 2939164}, {'score': 0.1111111111111111, 'name': 'wikileaks', 'size': 2421578}, {'score': 0.5, 'name': 'NickKristof', 'size': 1524875}, {'score': 0.3225806451612903, 'name': 'YourAnonNews', 'size': 1326974}, {'score': 0.0, 'name': 'Medium', 'size': 1000838}, {'score': 1.0, 'name': 'MotherJones', 'size': 454253}, {'score': 0.75, 'name': 'HuffPostPol', 'size': 434839}, {'score': 0.5, 'name': 'kanter', 'size': 404477}, {'score': 0.0, 'name': 'democracynow', 'size': 346634}, {'score': 0.75, 'name': 'ajam', 'size': 234583}, {'score': 0.5882352941176471, 'name': 'ACLU', 'size': 215687}, {'score': 0.0, 'name': 'RBReich', 'size': 213959}, {'score': 0.7777777777777778, 'name': 'OccupyWallSt', 'size': 205459}, {'score': 0.0, 'name': '99u', 'size': 189220}, {'score': 0.2727272727272727, 'name': 'pewresearch', 'size': 180915}, {'score': 0.0, 'name': 'iraglass', 'size': 114671}, {'score': 0, 'name': 'UpshotNYT', 'size': 99127}, {'score': 0.5, 'name': 'AlterNet', 'size': 85775}, {'score': 0.0, 'name': 'GA', 'size': 72842}, {'score': 0.25, 'name': 'Revkin', 'size': 63461}, {'score': 0.0, 'name': 'GirlsWhoCode', 'size': 60670}, {'score': 0.0, 'name': 'TheMoth', 'size': 56417}, {'score': 0.5, 'name': 'GlobalRevLive', 'size': 46053}, {'score': 0.0, 'name': 'earthisland', 'size': 43228}, {'score': 0.0, 'name': 'tomtomorrow', 'size': 42904}, {'score': 0.5, 'name': 'KQED', 'size': 42832}, {'score': 0.38181818181818183, 'name': 'OccupyOakland', 'size': 41277}, {'score': 0.14285714285714285, 'name': 'SaveManning', 'size': 39000}, {'score': 0.16666666666666666, 'name': 'Daily_Good', 'size': 36028}, {'score': 0.2, 'name': 'FoodCorps', 'size': 33166}, {'score': 0.0, 'name': 'FactTank', 'size': 26958}, {'score': 0.0, 'name': 'girldevelopit', 'size': 19839}, {'score': 0.038461538461538464, 'name': 'ProfessorCrunk', 'size': 17982}, {'score': 0.3333333333333333, 'name': 'quinnnorton', 'size': 17742}, {'score': 0.5, 'name': 'neworganizing', 'size': 17583}, {'score': 0.0, 'name': 'MattBors', 'size': 16922}, {'score': 0.0, 'name': 'aaronsw', 'size': 14894}, {'score': 0, 'name': 'KuraFire', 'size': 13236}, {'score': 0.5714285714285714, 'name': 'susie_c', 'size': 12590}, {'score': 0.1875, 'name': 'realfoodnow', 'size': 12550}, {'score': 0, 'name': 'hypatiadotca', 'size': 12081}, {'score': 0.0, 'name': 'dnbornstein', 'size': 10046}, {'score': 0.0, 'name': 'PopUpMag', 'size': 8707}, {'score': 0.0, 'name': 'sarahjeong', 'size': 8395}, {'score': 0, 'name': 'geekfeminism', 'size': 7809}]})

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
		print friend.SCREEN_NAME, friend.NUM_FOLLOWERS
		# print "friend created"
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

	sorted_by_influence = sorted(friendlist, key=lambda x: x.NUM_FOLLOWERS, reverse=True)
	friendlist = sorted_by_influence[:count]

	return friendlist

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

if __name__ == "__main__":
	app.run(debug=True)
