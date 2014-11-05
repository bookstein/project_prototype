from flask import Flask, request, render_template, redirect
import os
import prototype

app = Flask(__name__)
# TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
# TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
# TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
# TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		print "posting"
		screen_name = request.form.get("screenname")
		print screen_name
		friends = prototype.get_friends(screen_name)
		print friends #errors!
		# this worked in python interpreter: flask_server.prototype.get_friends("bookstein")

		# scored_friends = prototype.assign_all_friend_scores(friends)
		# print scored_friends
		return redirect("/")
	pass



if __name__ == "__main__":
	app.run(debug=True)