import os
import logging
import time, threading

from flask import Flask, request, render_template, redirect
import tweepy

from friends import User

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

TIME_TO_WAIT = 900/180 # 15 minutes divided into 180 requests
NUM_RETRIES = 2
RATE_LIMITED_RESOURCES =[("statuses", "/statuses/user_timeline")]

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/test.json")
def test_json():
	# Or - just do an object2json function of some sort and there's a shortcut to return that
	return render_template("test.json", obj_list = [{'handle': '@whoever', 'score': 10}, {'handle': '@blah', 'score': 20}])

@app.route("/display", methods=["GET", "POST"])
def display_friends():
	if request.method == "POST":
		screen_name = request.form.get("screenname")
		print screen_name
		api = connect_to_API()

		user = User(api, central_user=screen_name, user_id=screen_name)
		print user.SCORE

		try:
			friends_ids = user.get_friends_ids(screen_name)
			print friends_ids

			friendlist = []

			for page in user.paginate_friends(friends_ids, 100):
				process_friend_batch(user, page, api)

			return render_template("index.html", display = friendlist)


		except tweepy.TweepError as e:
			print "ERROR!!!!!", e
			# if e.message[0]["code"] == 88:
			# # {"errors":[{"message":"Rate limit exceeded","code":88}]}
			# 	print "EXCEEDED RATE LIMIT", e

			return render_template("index.html", display = e)

def process_friend_batch(user, page, api):
	friend_objs = user.lookup_friends(f_ids=page)
	for f in friend_objs:
		friend = User(user_id=f.id, api=api)
		print friend.SCORE

def check_rate_limit(api):
		limits = api.rate_limit_status()
		stats = limits["resources"]["statuses"]
		for resource in stats.keys():
			if stats[resource]["remaining"] < 2:
				print "EXPIRED:", resource
			else:
				print resource, ": rate limit not exceeded"
		threading.Timer(self.TIME_TO_WAIT, self.check_rate_limit).start()
		# check rate limit for a given resource instead of hardcoding

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
	api = tweepy.API(auth, cache=None) #removed wait_on_rate_limit=True, wait_on_rate_limit_notify=True

	return api

if __name__ == "__main__":
	app.run(debug=True)