import os
import logging

from flask import Flask, request, render_template, redirect
import tweepy

from friends import User

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

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
		print "posting"
		screen_name = request.form.get("screenname")
		print screen_name
		# me = tw_api.get_user_by_id(screen_name)
		# print me
		api = connect_to_API()
		user = User(api=api, screen_name=screen_name)
		user.USER_SCORE = user.score_user()

		try:
			friends_ids = user.get_friends_ids(screen_name)
			print friends_ids

			friendlist = []

			for page in user.paginate_friends(friends_ids, 100):
				friend_objs = user.lookup_friends(f_ids=page)
				for f in friend_objs:
					friend = User(api=api, screen_name=f.id)
					friend_timeline = friend.get_timeline(f.id, 100)
					print friend_timeline
					# friend.USER_SCORE = friend.score_user()
					# friendlist.append(friend.USER_SCORE)

			return render_template("index.html", display = friendlist)


		except Exception as e:
			print "ERROR!!!!!", e
			return render_template("index.html", display = e)



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