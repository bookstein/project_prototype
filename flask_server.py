import os
import json
import datetime
import time
import cPickle as pickle

from flask import Flask, url_for, request, render_template, redirect, flash
import tweepy

from friends import User, check_rate_limit
import politwit.model as model

app = Flask(__name__)
app.secret_key = 'politicaltwitter'


TIME_TO_WAIT = 900/180 # 15 minutes divided into 180 requests
NUM_RETRIES = 2

PATH_TO_VECTORIZER = "politwit/vectorizer.pkl"
PATH_TO_CLASSIFIER = "politwit/classifierNB.pkl"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/ajax/user", methods=["POST"])
def get_user():
	api = connect_to_API()

	screen_name = request.json["screen_name"]

	if screen_name == "bookstein":
		return redirect("/ajax/testing")

	try:
		# check to make sure this user exists before proceeding
		user = api.get_user(screen_name=screen_name, include_entities=False)
		if user.id_str:
			return redirect(url_for("display_friends", screen_name=screen_name))
		else:
			flash("Twitter couldn't find that username. Please try again!", "Error")
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

	try:
		friends_ids = user.get_friends_ids(screen_name)

		friendlist = [user]

		for page in user.paginate_friends(friends_ids, 100):
			friends = process_friend_batch(user, page, api)
			friendlist.extend(friends)

		if len(friendlist) > user.MAX_NUM_FRIENDS:
			friendlist = get_top_influencers(friendlist, user.MAX_NUM_FRIENDS)

	except tweepy.TweepError as e:
		error_message = handle_error(e)
		flash(error_message)
		return redirect(url_for("index"))

	# initialized friend_scores object with root, children
	friend_scores = {"name": user.USER_ID, "children": []}

	try:
		for friend in friendlist:
			timeline = friend.get_timeline(friend.USER_ID, friend.MAX_NUM_TWEETS)
			friend.SCORE = friend.score(timeline, vectorizer, classifier)

			friend_scores["children"].append({"name": friend.SCREEN_NAME, "size": friend.NUM_FOLLOWERS, "score": friend.SCORE})

	except tweepy.TweepError as e:
		error_message = handle_error(e)
		flash(error_message)
		return redirect(url_for("index"))

	if len(friend_scores) > 0:
		json_scores = json.dumps(friend_scores)
		return json_scores

	else:
		return redirect("/")#, add flash --> errormessage="Unable to get friends")

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

	sorted_by_influence = sorted(friendlist, key=lambda x: x.NUM_FOLLOWERS, reverse=True)
	friendlist = sorted_by_influence[:count]

	return friendlist

@app.route("/ajax/testing")
def test_results():
	return json.dumps({'name': 'bookstein', 'children': [{'score': 0.6621288434149878, 'name': 'nytimes', 'size': 14160089}, {'score': 0.6024210739190844, 'name': 'DalaiLama', 'size': 9834809}, {'score': 0.7532961655655628, 'name': 'BBCWorld', 'size': 8049266}, {'score': 0.7170098613172879, 'name': 'nprnews', 'size': 3061375}, {'score': 0.7411111088037284, 'name': 'maddow', 'size': 3044201}, {'score': 0.668490765740428, 'name': 'TheDailyShow', 'size': 2944827}, {'score': 0.6106084371672981, 'name': 'wikileaks', 'size': 2423037}, {'score': 0.7844805290743996, 'name': 'NickKristof', 'size': 1525849}, {'score': 0.9214918901147827, 'name': 'YourAnonNews', 'size': 1326447}, {'score': 0.3957033176556604, 'name': 'Medium', 'size': 1002287}, {'score': 0.8745964630221176, 'name': 'MotherJones', 'size': 455471}, {'score': 0.9478069469237381, 'name': 'HuffPostPol', 'size': 435314}, {'score': 0.4862231158061716, 'name': 'kanter', 'size': 404467}, {'score': 0.8444930591757265, 'name': 'democracynow', 'size': 347059}, {'score': 0.9260415189549398, 'name': 'ajam', 'size': 235139}, {'score': 0.9462528483917902, 'name': 'ACLU', 'size': 215827}, {'score': 0.9063116375558954, 'name': 'RBReich', 'size': 214252}, {'score': 0.8708490825538281, 'name': 'OccupyWallSt', 'size': 205603}, {'score': 0.43175795370399034, 'name': '99u', 'size': 189275}, {'score': 0.7244459940118697, 'name': 'pewresearch', 'size': 181212}, {'score': 0.6005260246749018, 'name': 'iraglass', 'size': 115326}, {'score': 0.8172435268595505, 'name': 'UpshotNYT', 'size': 99405}, {'score': 0.8154697883980356, 'name': 'AlterNet', 'size': 85902}, {'score': 0.2793861118514671, 'name': 'GA', 'size': 72873}, {'score': 0.6255953154263557, 'name': 'Revkin', 'size': 63501}, {'score': 0.3344072389905702, 'name': 'GirlsWhoCode', 'size': 61199}, {'score': 0.31305912636044037, 'name': 'TheMoth', 'size': 56476}, {'score': 0.9687524863997323, 'name': 'GlobalRevLive', 'size': 46335}, {'score': 0.5585787738587116, 'name': 'earthisland', 'size': 43248}, {'score': 0.5753698699586668, 'name': 'KQED', 'size': 42924}, {'score': 0.5769960776462038, 'name': 'tomtomorrow', 'size': 42916}, {'score': 0.8971033977000994, 'name': 'OccupyOakland', 'size': 41415}, {'score': 0.9102259061950695, 'name': 'SaveManning', 'size': 39019}, {'score': 0.27995737240395124, 'name': 'Daily_Good', 'size': 36056}, {'score': 0.3492342885188048, 'name': 'FoodCorps', 'size': 33250}, {'score': 0.8744117577919912, 'name': 'FactTank', 'size': 27073}, {'score': 0.3416501953318024, 'name': 'girldevelopit', 'size': 19914}, {'score': 0.7514660970444359, 'name': 'ProfessorCrunk', 'size': 18090}, {'score': 0.5843995473438215, 'name': 'quinnnorton', 'size': 17763}, {'score': 0.866547681131552, 'name': 'neworganizing', 'size': 17588}, {'score': 0.49393225605868346, 'name': 'MattBors', 'size': 16939}, {'score': 0.6116565283368856, 'name': 'aaronsw', 'size': 14906}, {'score': 0.7549212121248698, 'name': 'KuraFire', 'size': 13239}, {'score': 0.7790318818514511, 'name': 'susie_c', 'size': 12601}, {'score': 0.4780180119515844, 'name': 'realfoodnow', 'size': 12562}, {'score': 0.5764062616942909, 'name': 'hypatiadotca', 'size': 12090}, {'score': 0.6052069259993499, 'name': 'dnbornstein', 'size': 10058}, {'score': 0.24306846602456034, 'name': 'PopUpMag', 'size': 8707}, {'score': 0.6653150003042494, 'name': 'sarahjeong', 'size': 8388}, {'score': 0.2934325219344482, 'name': 'geekfeminism', 'size': 7826}]})

def handle_error(e):
	if e.args[0][0]['code'] == "88":
		return "Rate limit exceeded: please wait a few minutes to retry."
	else:
		return "Error: We encountered an error while contacting Twitter: \n" + e.args[0][0]["message"]


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
