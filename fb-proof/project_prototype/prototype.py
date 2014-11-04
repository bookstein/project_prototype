import json
import requests
import random
from flask import Flask, render_template
import facebook

app = Flask(__name__)

# extended permissions granted in this token
TOKEN = "CAACEdEose0cBAB7ZBNzW1T43H5ZB4qGUJqSvf10vuvMm4DFvZCXywHmcyKC6sfHbdL68vaTf0ohuDZAMTe8a2NhWfDxBw1azVSpbmZAf8nZBzLXDFjq1YdvlYngNjEhRuZCC9o88YkJVWuBWXsM11tOwlRh7VeprDQJ8muCXQP93LpZBugSD45lXqfNLGQoZB5uCCcINFbnh3qaMccQ8rfqbJPtZAI9dWXDDYZD"
ME = 10204233350047567
g = facebook.GraphAPI(TOKEN)

@app.route("/")
def index():
    return render_template("fb-test.html")

def print_as_json(obj):
    print json.dumps(obj, indent=1)

def user_likes_page(user_id, page_id):
    """returns whether a user likes a page"""

    url = "https://graph.facebook.com/%d/likes/%d" % (user_id, page_id)
    parameters = {"access_token": TOKEN}
    r = requests.get(url, params = parameters)
    result = json.loads(r.text)
    print result

    if result.get("data"):
        print True
    else:
        print False



def get_feed():
    """returns user feed (all timeline posts)"""

    parameters = {'access_token': TOKEN}
    r = requests.get('https://graph.facebook.com/me/feed', params=parameters)
    result = json.loads(r.text)
    print result['data']


def all_friends():
    """ returns a list of all friends
    with limit 5 friends: /v2.2/me/?fields=friends.limit(5)"""

    parameters = {"access_token": TOKEN}
    r = requests.get('https://graph.facebook.com/me?fields=friends.limit(5)', params=parameters)
    result = json.loads(r.text)
    if result.get("friends"):
        return result["friends"]["data"]

    else:
        print "No friends found"
        return None

def are_we_friends(friend_id):
    """ returns True or False of whether or not we are friends """
    parameters = {"access_token": TOKEN}
    url = "https://graph.facebook.com/%d/friends/%d" % (ME, int(friend_id))
    r = requests.get(url, params = parameters)
    result= json.loads(r.text)

    if result.get("data"):
        print "We are friends"
        return True
    else:
        print "Not friends"
        return False

def find_links_in_feed(user_id):
    """ shows links published by a person. (Only people who have given permission to the app.)"""
    # very similar request and data structure as getting friends list!

    parameters = {"access_token": TOKEN}
    url = 'https://graph.facebook.com/%d?fields=links.limit(3)' % user_id
    r = requests.get(url, params=parameters)
    result = json.loads(r.text)
    if result.get("links"):
        # print result["links"]["data"]
        # for link_obj in result["links"]["data"]:
            # print link_obj["link"] # prints only the links user has posted
        return result["links"]["data"]
    else:
        print "No links found"
        return None

def people_who_liked_my_post(user_id):
    """gets list of people who have liked my posts"""
    print "running"
    links = find_links_in_feed(user_id) # returns link data
    link = links[1] # get a link that has Likes
    people = []
    for liker in link["likes"]["data"]:
        people.append(liker)
    print people
    return people

def get_friend_likes():
    # returns list of friend objects from "data" key
    friends = g.get_connections("me", "friends")["data"]

    # dictionary comprehension! likes for 1 friend (via slicing)
    likes = { friend["name"]:
        g.get_connections(friend["id"], "likes")["data"]
        for friend in friends[:1] }

    print likes # this is a dictionary

def main():
    # TESTING MY FUNCTIONS:
    # user_likes_page(ME, 23028125953)
    # get_feed()
    # friend_id = all_friends()[0]["id"] # gets first friend id
    # random_id = random.randint(0, 1000000) # gets random id
    # another_friend_id =  4801712
    # print random_id
    # are_we_friends(friend_id)
    # are_we_friends(random_id)
    # are_we_friends(another_friend_id) # even with limit(5), function knows this ID is further in list of friends
    # find_links_in_feed(ME)
    # people_who_liked_my_post(ME)

    # USING PYTHON SDK:
    # print_as_json(g.get_object('me'))
    # print_as_json(g.get_connections('me', 'friends'))
    # print_as_json(g.request("search", {'q': 'voting', 'type': 'page'}))
    # get_friend_likes()
    print all_friends()


if __name__ == "__main__":
    # app.run(debug=True)
    main()
