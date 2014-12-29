import sys
import unittest
from mock import Mock, patch, ANY

sys.path.append("../")
import politwit.friends as friends


class TestFriends(unittest.TestCase):
    def setUp(self):
        """Create mock tweepy with patch"""
        patcher = patch("politwit.friends.tweepy")

        self.mock_tweepy = patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        pass

    def test_get_friends_ids(self):

        test_username = "bookstein"

        api_spec = ["friends_ids"]
        mock_api = Mock(name="tweepy_api", spec=api_spec)
        # creates mock object

        user = friends.User(api=mock_api, user_id=test_username,
                            central_user=test_username)
                            # create user with mock api object

        result = user.get_friends_ids()

        print "result", result

        print "mock calls to api:", mock_api.mock_calls
        mock_api.friends_ids.assert_called_with(screen_name=test_username)
        print "mock api", mock_api

        print "\n***********************"

if __name__ == "__main__":
    unittest.main()
