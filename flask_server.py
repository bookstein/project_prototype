from flask import Flask, request, render_template, redirect
import os
from friends import User
import logging
import itertools

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

		try:
			friend_ids = user.get_friend_ids(screen_name)
			print friends_ids, len(friends_ids)

			# if len(friends_ids) > 100:
			# 	user.get_top_influencers(friends_ids)


			friendlist = []

			# for friend in friends_ids:
			#     friend = User()
			#     friend.USER_SCORE = friend.score_user()
			#     friendlist.append(friend)

			for page in paginate_friends(friends_ids, 100):
				print page
				for friend in page:
					friendlist.append(friend)


			# print "friendlist", friendlist

			# for friend in friendlist:
			#     print "friend=", friend

			return render_template("index.html", display = friendlist)


		except Exception as e:
			print "ERROR!!!!!", e
			return render_template("index.html", display = e)

def paginate_friends(ids, page_size):
    print "working!"
    while True:
        iterable1, iterable2 = itertools.tee(ids)
        ids, page = (itertools.islice(iterable1, page_size, None),
                list(itertools.islice(iterable2, page_size)))
        if len(page) == 0:
            break
        # yield is a generator keyword
        yield page


if __name__ == "__main__":
	app.run(debug=True)