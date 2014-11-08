from os import path, makedirs
import tw_api
import json
import time

TEST = ["bookstein"]
USERS = ["maddow", "rushlimbaugh", "MatthewKeysLive", "iamjohnoliver",
"SenRandPaul"]

def get_rate_limit_status():
	"""
	Logs "statuses" rate limit status to a log file.
	Returns remaining number of API calls, per Twitter rate limits, for resource family of statuses.

	See Twitter API docs: https://dev.twitter.com/rest/reference/get/application/rate_limit_status
	"""
	log = open("rate_limit_log.txt", "a+")
	status = tw_api.api.rate_limit_status(resources="statuses")
	remaining = status["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
	log.write("STATUS \n\n" + str(status) + "\n\n")
	log.close()
	return remaining

def make_friends_list(username):
	FRIENDS = tw_api.get_friends(username)
	return FRIENDS


def make_feed_file(username, friend="self"):
	if not path.isdir("json/"+username):
		makedirs("json/"+username)
		print "directory made!"

	filename = "json/"+username+"/"+str(friend)+".json"

	if not path.isfile(filename):
		if friend == "self":
			write_to_file(filename, username)
		else:
			write_to_file(filename, friend)
	else:
		print filename, " already exists"

def write_to_file(filename, user):
	# for transferring chunks of data at a time to file
	status_list = [] # this is the same concept as a "page"
	# counter
	n = 0

	outfile = open(filename, "a+")

	# gets most recent 100 tweets from user's timeline
	feed = tw_api.get_timeline(user, 100)

	for status in feed:
		if get_rate_limit_status() > 0:
			print n, "\n\n", status, "\n\n"
			status_list.append(status._json)
			n += 1
		else:
			print get_rate_limit_status(), "\n\nleft off at ", n

	outfile.write(json.dumps(status_list))
	outfile.close()

## IMITATE THIS? ##
# c = tweepy.Cursor(api.search, <--- this goes into get_timeline
#                        q=search,
#                        include_entities=True).items()
# while True:
#     try:
#         tweet = c.next()
#         # Insert into db
#     except tweepy.TweepError:
#         time.sleep(60 * 15)
#         continue
#     except StopIteration:
#         break


def main():
	# make_feed_file("bookstein")
	get_rate_limit_status()
	for username in TEST:
		# make dir to hold all relevant files, add file for user
		make_feed_file(username)
		# get list of all friends by user's id
		friends_list = make_friends_list(username)

		# friends_list was truncated to [:50] when making celebrity files!! Shoot.
		for friend_id in friends_list:
			# friend = tw_api.get_user_by_id(friend_id)
			# make file for friend in directory {username}
			make_feed_file(username, friend_id)

if __name__ == "__main__":
	tw_api.init_api()
	main()