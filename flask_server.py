import os
import logging
import time#, threading
import json
import datetime

from flask import Flask, url_for, request, render_template, redirect, flash
import tweepy

from friends import User
import model

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

	friend_scores = list()

	try:
		for friend in friendlist:
			timeline = friend.get_timeline(friend.USER_ID, friend.MAX_NUM_TWEETS)
			# logging.info("Friend timeline request: \n", check_rate_limit(api))
			print check_rate_limit(api)
			# print retrieve_remaining_requests(api)

			hashtag_count = friend.count_hashtags(timeline)
			friend.SCORE = friend.score(hashtag_count, political_hashtags_dict)

			friend_scores.append({"screen_name": friend.SCREEN_NAME, "followers": friend.NUM_FOLLOWERS, "score": friend.SCORE})

			# friend_scores[friend.SCREEN_NAME] = {"followers": friend.NUM_FOLLOWERS, "score": friend.SCORE}

	except tweepy.TweepError as e:
		print "ERROR!!!!!", e
		# logging.warning("ERROR: \n", check_rate_limit(api))

	if len(friend_scores) > 0:
		print "FRIEND SCORES", friend_scores
		json_scores = json.dumps(friend_scores)
		# json_scores = [json.dumps(score_obj) for score_obj in friend_scores]
		return json_scores

	else:
		return redirect("/")#, add flash --> errormessage="Unable to get friends")

@app.route("/ajax/tweets", methods=["GET", "POST"])
def get_latest_tweets():
	# user = User(api, user_id=screen_name)
	# tweets = user.get_timeline(user.USER_ID, 5)
	screen_name = request.json["screen_name"]
	print "SCREEN NAME FOR TWEETS", screen_name
	tweets = [{"text": "Hi"},{"text": "Oh my gosh what an amazing day #yolo"}, {"text": "#Ferguson"}]
	json_tweets = json.dumps(tweets)
	return json_tweets

@app.route("/ajax/testing")
def test_results():
	return json.dumps([{'score': 0, 'followers': 14121834, 'screen_name': 'nytimes'}, {'score': 0, 'followers': 9814948, 'screen_name': 'DalaiLama'}, {'score': 0.2, 'followers': 8023469, 'screen_name': 'BBCWorld'}, {'score': 0.0, 'followers': 3052266, 'screen_name': 'nprnews'}, {'score': 1.0, 'followers': 3041963, 'screen_name': 'maddow'}, {'score': 0.0, 'followers': 2936642, 'screen_name': 'TheDailyShow'}, {'score': 0.1111111111111111, 'followers': 2420696, 'screen_name': 'wikileaks'}, {'score': 0.125, 'followers': 1524481, 'screen_name': 'NickKristof'}, {'score': 0.4166666666666667, 'followers': 1326347, 'screen_name': 'YourAnonNews'}, {'score': 0.0, 'followers': 1000101, 'screen_name': 'Medium'}, {'score': 1.0, 'followers': 453768, 'screen_name': 'MotherJones'}, {'score': 1.0, 'followers': 434682, 'screen_name': 'HuffPostPol'}, {'score': 0.3333333333333333, 'followers': 404473, 'screen_name': 'kanter'}, {'score': 0.3333333333333333, 'followers': 346444, 'screen_name': 'democracynow'}, {'score': 1.0, 'followers': 234337, 'screen_name': 'ajam'}, {'score': 0.5882352941176471, 'followers': 215619, 'screen_name': 'ACLU'}, {'score': 0.0, 'followers': 213864, 'screen_name': 'RBReich'}, {'score': 0.7777777777777778, 'followers': 205366, 'screen_name': 'OccupyWallSt'}, {'score': 0.0, 'followers': 189192, 'screen_name': '99u'}, {'score': 0.5, 'followers': 180794, 'screen_name': 'pewresearch'}, {'score': 0, 'followers': 114458, 'screen_name': 'iraglass'}, {'score': 0, 'followers': 98981, 'screen_name': 'UpshotNYT'}, {'score': 0.42857142857142855, 'followers': 85748, 'screen_name': 'AlterNet'}, {'score': 0.0, 'followers': 72823, 'screen_name': 'GA'}, {'score': 0.2727272727272727, 'followers': 63441, 'screen_name': 'Revkin'}, {'score': 0.0, 'followers': 60414, 'screen_name': 'GirlsWhoCode'}, {'score': 0.0, 'followers': 56396, 'screen_name': 'TheMoth'}, {'score': 0.28, 'followers': 45983, 'screen_name': 'GlobalRevLive'}, {'score': 0.0, 'followers': 43212, 'screen_name': 'earthisland'}, {'score': 0.0, 'followers': 42887, 'screen_name': 'tomtomorrow'}, {'score': 0.35714285714285715, 'followers': 42822, 'screen_name': 'KQED'}, {'score': 0.3469387755102041, 'followers': 41217, 'screen_name': 'OccupyOakland'}, {'score': 0.14285714285714285, 'followers': 38990, 'screen_name': 'SaveManning'}, {'score': 0.16666666666666666, 'followers': 36025, 'screen_name': 'Daily_Good'}, {'score': 0.2, 'followers': 33145, 'screen_name': 'FoodCorps'}, {'score': 1.0, 'followers': 26905, 'screen_name': 'FactTank'}, {'score': 0.0, 'followers': 19821, 'screen_name': 'girldevelopit'}, {'score': 0.05263157894736842, 'followers': 17951, 'screen_name': 'ProfessorCrunk'}, {'score': 0.8, 'followers': 17748, 'screen_name': 'quinnnorton'}, {'score': 0.5, 'followers': 17579, 'screen_name': 'neworganizing'}, {'score': 0, 'followers': 16908, 'screen_name': 'MattBors'}, {'score': 0.0, 'followers': 14888, 'screen_name': 'aaronsw'}, {'score': 0.0, 'followers': 13235, 'screen_name': 'KuraFire'}, {'score': 0.0, 'followers': 12592, 'screen_name': 'susie_c'}, {'score': 0.1875, 'followers': 12548, 'screen_name': 'realfoodnow'}, {'score': 0, 'followers': 12076, 'screen_name': 'hypatiadotca'}, {'score': 0.0, 'followers': 10044, 'screen_name': 'dnbornstein'}, {'score': 0.0, 'followers': 8705, 'screen_name': 'PopUpMag'}, {'score': 0.6666666666666666, 'followers': 8399, 'screen_name': 'sarahjeong'}, {'score': 0, 'followers': 7795, 'screen_name': 'geekfeminism'}])

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
