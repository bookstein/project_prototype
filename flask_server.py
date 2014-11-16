from flask import Flask, request, render_template, redirect
import os
import friends
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/display", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		print "posting"
		screen_name = request.form.get("screenname")
		print screen_name
		# me = tw_api.get_user_by_id(screen_name)
		# print me
		user = friends.User()
		user.CURRENT_USER = screen_name
		friendlist = user.get_friend_ids(screen_name)
		print friendlist
		#error: this worked in python interpreter: flask_server.tw_api.get_friends("bookstein")

		# scored_friends = tw_api.assign_all_friend_scores(friends)
		# print scored_friends
		return render_template("index.html", friends = friendlist)
	pass



if __name__ == "__main__":
	app.run(debug=True)