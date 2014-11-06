# import model
import prototype
import json

USERS = ["bookstein", "maddow", "rushlimbaugh", "MatthewKeysLive", "iamjohnoliver",
"SenRandPaul"]

def make_feed_file(username):
	prototype.init_api()
	outfile = open("tweetfiles/"+username+".json", "a+")
	feed = prototype.get_timeline(username, 400)
	for status in feed:
		outfile.write(json.dumps(status._json))
	outfile.close()
	# return feed

def main():
	for name in USERS:
		make_feed_file(name)

if __name__ == "__main__":
	main()