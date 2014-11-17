from flask import Flask, request, render_template, redirect
import os
from friends import User
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/display", methods=["GET", "POST"])
def display_friends():
	if request.method == "POST":
		print "posting"
		screen_name = request.form.get("screenname")
		print screen_name
		# me = tw_api.get_user_by_id(screen_name)
		# print me
		user = User()
		user.CURRENT_USER = screen_name
		user.USER_SCORE = user.score_user()

		friendlist = user.get_friend_ids(screen_name)
		print friendlist



		return render_template("index.html", friends = friendlist)




if __name__ == "__main__":
	app.run(debug=True)