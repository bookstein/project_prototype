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

        # TODO: test this where friend ids is > 5000
        # will cause Twitter error because I'm not using Cursor

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

    def test_lookup_friends(self):

        # ARRANGE
        test_username = "bookstein"
        test_friends_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
        ,32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,48, 49
        , 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,64, 65, 66,
        67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82
        ,83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]

        api_spec = ["lookup_users"]
        mock_api = Mock(name="tweepy_api", spec=api_spec)

        user = friends.User(api=mock_api, user_id=test_username,
                            central_user=test_username)
                            # create user with mock api object
        # ACT
        result = user.lookup_friends(test_friends_ids)

        # ASSERT
        print "result", result
        print "mock calls to api:", mock_api.mock_calls
        mock_api.lookup_users.assert_called_with(test_friends_ids)
        print "mock api", mock_api

        print "\n***********************"

    def test_get_timelines(self):
        # ARRANGE
        test_username = "bookstein"

        api_spec = ["user_timeline"]
        mock_api = Mock(name="tweepy_api", spec=api_spec)

        user = friends.User(api=mock_api, user_id=test_username,
                            central_user=test_username)
                            # create user with mock api object

        # mock Cursor on tweepy (tweepy.Cursor)
        cursor_mock = self.mock_tweepy.Cursor.return_value
        #cursor_mock.items.return_value = []

        # ACT
        result = user.get_timeline(20)

        # ASSERT
        print "result", result
        print "mock calls to api:", mock_api.mock_calls
        print "Cursor called with:", mock_tweepy.Cursor.assert_called_with(ANY)
        print "User_timeline called with:", mock_api.user_timeline.assert_called_with(id=user.user_id)

        print "\n***********************"

if __name__ == "__main__":
    unittest.main()
