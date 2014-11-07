from os import path, makedirs
import tw_api
import json

TEST = ["bookstein"]
USERS = ["bookstein", "maddow", "rushlimbaugh", "MatthewKeysLive", "iamjohnoliver",
"SenRandPaul"]

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
		print "file already exists"

def write_to_file(filename, user):
	outfile = open(filename, "a+")
	feed = tw_api.get_timeline(user, 400)
	n = 0
	for status in feed:
		print n, "\n\n", status, "\n\n"
		outfile.write(json.dumps(status._json))
		n += 1
	outfile.close()

def main():
	# make_feed_file("bookstein")
	for username in TEST:
		# make dir to hold all relevant files, add file for user
		make_feed_file(username)
		# get list of all friends by user's id
		friends_list = make_friends_list(username)
		# print friends_list
		for friend_id in friends_list[:2]:
			# friend = tw_api.get_user_by_id(friend_id)
			# make file for friend in directory {username}
			make_feed_file(username, friend_id)

if __name__ == "__main__":
	tw_api.init_api()
	main()