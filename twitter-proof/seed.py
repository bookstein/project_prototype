from os import path, makedirs
import tw_api
import json

USERS = ["bookstein", "maddow", "rushlimbaugh", "MatthewKeysLive", "iamjohnoliver",
"SenRandPaul"]

def make_friends_list(username):
	FRIENDS = tw_api.get_friends(username)
	return FRIENDS


def make_feed_file(username, friend="self"):
	if not path.isdir("json/"+username):
		makedirs("json/"+username)
		print "directory made!"

	outfile = open("json/"+username+"/"+friend+".json", "a+")
	feed = tw_api.get_timeline(username, 400)
	for status in feed:
		outfile.write(json.dumps(status._json))
	outfile.close()

def main():
	make_feed_file("bookstein")
	# for name in USERS[0]:
	# 	friends_list = make_friends_list(name)
	# 	for friend_id in friends_list:
	# 		friend = tw_api.get_user_by_id(friend_id)
	# 		make_feed_file(friend.screen_name)

if __name__ == "__main__":
	tw_api.init_api()
	main()