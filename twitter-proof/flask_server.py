from flask import Flask, request, render_template, redirect
import os
import tw_api
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		print "posting"
		screen_name = request.form.get("screenname")
		print screen_name
		# me = tw_api.get_user_by_id(screen_name)
		# print me
		tw_api.init_api()
		friends = tw_api.get_friends(screen_name)
		print friends
		#error: this worked in python interpreter: flask_server.tw_api.get_friends("bookstein")

		# scored_friends = tw_api.assign_all_friend_scores(friends)
		# print scored_friends
		return render_template("index.html", friends = friends)
	pass



if __name__ == "__main__":
	app.run(debug=True)