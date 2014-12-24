import sys
import unittest
from mock import Mock, patch, ANY

sys.path.append("../")
import politwit.friends as friends

print "imports done"

class TestFriends(unittest.TestCase):
    def setUp(self):
        print "starting set up"

        patcher = patch("politwit.friends.tweepy")

        print "patch made"

        self.mock_tweepy = patcher.start()

        self.addCleanup(patcher.stop)

    def tearDown(self):
        pass

    def test_get_friends_ids(self):

        mock_api = Mock(name="tweepy_api") # creates mock object
        user = friends.User(api=mock_api, user_id="bookstein", central_user="bookstein") # create user with mock api object

        result = user.get_friends_ids()

        print result

        print self.mock_tweepy.mock_calls

        print mock_api

        print "\n***********************"

if __name__ == "__main__":
    unittest.main()
