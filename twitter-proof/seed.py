from os import path, makedirs
import tw_api
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
	rate_info = tw_api.api.rate_limit_status()['resources']
	initial_rate_limit = int(rate_info[resource_family][resource]["remaining"])
	return initial_rate_limit

# def watch_rate_limit(rate_limit, n=0):
# 	"""Use initial rate limit from check_rate_limit_status to count down until rate limit is exhausted
# 		Returns remaining number of API calls for given resource
# 	"""
# 	return rate_limit - n

def make_friends_list(username):
	FRIENDS = tw_api.get_friends(username)
	return FRIENDS


def make_feed_file(username, friend="self"):

	if not path.isdir("json2/"+username):
		makedirs("json2/"+username)
		print "directory made!"

	filename = "json2/"+username+"/"+str(friend)+".json"


	if not path.isfile(filename):
		if friend == "self":
			write_to_file(filename, username)
		else:
			write_to_file(filename, friend)
	else:
		print filename, " already exists"

def write_to_file(filename, user):
	"""

	Write feed to file, one status at a time -- versus in a chunk?? Removed status_list list because if program errors, API calls would be in vain... WIP

	"""
	# for transferring chunks of data at a time to file
	# status_list = [] # this is the same concept as a "page"
	rate_limit = check_rate_limit_status("statuses", "/statuses/user_timeline")
	# initialize counter
	n = 0

	with open(filename, "a+") as outfile:
		# gets most recent 100 tweets from user's timeline
		feed = tw_api.get_timeline(user, 100)

		for status in feed:
			if n < rate_limit:
				print n, "\n\n", status, "\n\n"
				# status_list.append(status._json)
				outfile.write(json.dumps(status._json))
				n += 1

			else:
				print "left off at ", n, "\n\n", status, "\n\n"


	# outfile.write(json.dumps(status_list))
	# outfile.close()


def main():
	# make_feed_file("bookstein")



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
	for username in USERS:
		make_feed_file(username)
	# main()

