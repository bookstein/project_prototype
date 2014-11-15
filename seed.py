from os import path, makedirs
import friends
import json
import time

TEST = ["bookstein"]
USERS = ["maddow", "rushlimbaugh"] #"MatthewKeysLive", "iamjohnoliver", "SenRandPaul"
TIME_TO_WAIT = 900 / 180

def check_rate_limit_status(resource_family, resource):
	"""
	Returns initial number of allowed API calls, per Twitter rate limits, for a given resource family and resource.
	Example: to check statuses (tweets), use resource family "statuses", resource "/statuses/user_timeline"

	For other resources, see Twitter API docs: https://dev.twitter.com/rest/reference/get/application/rate_limit_status
	"""
	rate_info = twitter_user.api.rate_limit_status()['resources']
	initial_rate_limit = int(rate_info[resource_family][resource]["remaining"])
	return initial_rate_limit


def make_friends_list(username):
	FRIENDS = twitter_user.get_friends(username)
	return FRIENDS


def make_feed_file(username, friend="self"):
	if not path.isdir("json/"+username):
		makedirs("json/"+username)
		print "directory made!"

	filename = "json/"+username+"/"+str(friend)+".json"

	if not path.isfile(filename):
		if friend == "self":
			write_to_file(filename, username)
			print friend
		else:
			write_to_file(filename, friend)
	else:
		print filename, " already exists"

def write_to_file(filename, user):
	"""
	Write feed to file. BUT if program errors, API calls would be in vain... WIP
	"""
	# for transferring chunks of data at a time to file
	# status_list = [] # this is the same concept as a "page"
	rate_limit = check_rate_limit_status("statuses", "/statuses/user_timeline")
	# initialize counter
	n = 0
	# array to hold JSON objects
	statuses_list = []

	with open(filename, "a+") as outfile:
		"""gets most recent 100 tweets from user's timeline"""
		statuses = twitter_user.get_timeline(user, 100)

		for status in statuses:
			if n < rate_limit:
				print n, "\n\n", status, "\n\n"
				n += 1
				statuses_list.append(status._json)
				# outfile.write(json.dumps(status._json, indent=1))
				# outfile.write("||") # delimiter for splitting on later
			else:
				print "left off at ", n, "\n\n", status, "\n\n"
				break

		outfile.write(json.dumps(statuses_list, indent=1))

	# outfile.write(json.dumps(status_list))
	# outfile.close()


def main():
	"""Full file setup for user and their friends"""
	for username in USERS:
		make_feed_file(username)
		friends_list = make_friends_list(username)

		for friend_id in friends_list:
			make_feed_file(username, friend_id)

if __name__ == "__main__":
	# instantiate user object, including api
	twitter_user = friends.User()
	for username in USERS:
		make_feed_file(username)
	# main()