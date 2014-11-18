#!/usr/bin/env python
'''
Author: Michael Ricks-Aherne

Unit testing of the friends module
'''

import sys
import unittest
from mock import Mock, patch, ANY
# quick hack to allow importing of friends.
# Don't do this outside of test code!
sys.path.append("..")
import friends


class TestFriends(unittest.TestCase):
    def setUp(self):
        # Things that happen before EVERY unit test go here

        # This is where I like to mock out 3rd party libraries.
        # The syntax is weird...

        # Tell patcher to patch out tweepy in the namespace of friends
        patcher = patch('friends.tweepy')

        # Assign a reference to the mocked out module, using self.xxx
        # so that the reference is available in each unit test
        self.mock_tweepy = patcher.start()

        # Be sure to unpatch the library, so that code from one test
        # doesn't leak onto another.
        self.addCleanup(patcher.stop)

    def tearDown(self):
        # Things that happen after EVERY unit test go here
        pass

    def test_example(self):
        print "test_example"
        # All tests must be named test_xyz.  I tend to use long names
        # that are like test_function_with_inputs_produces_expected_output
        # It's crazy long, but this function never has to be called test_get_friends_ids_calls_correct_methods
        # anywhere -- and if it breaks, the name will immediately tell
        # you the problem.

        # I also follow the ARRANGE-ACT-ASSERT pattern for unit testing.
        # See below...

        # ARRANGE
        mock_api = Mock()  # make a mock for the api
        user = friends.User(api=mock_api)  # Create the user object, using the mock
        # At this point we have 2 mocks: self.mock_tweepy and mock_api
        # These can be used to check different conditions.
        # First, we show what it's like without any special mock configuration

        # ACT
        result = user.get_friends_ids("userid")

        # ASSERT
        # Note a few things:
        #   result is itself a Mock: <MagicMock name='tweepy.Cursor().items()' id='12345678'>
        #      This is because all Mocks return Mocks, unless told to do something else
        #      So the call to tweepy.Cursor(...) returned a mock, because tweepy
        #      has been mocked
        print result
        # Note the calls to tweepy:
        print self.mock_tweepy.mock_calls
        # And note that while there were no calls to mock_api, an attribute
        # was accessed. You can see that in the calls to tweepy.
        print mock_api
        print "\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n" # space between tests

    def test_example_with_configuring_mocks(self):
        print "test_example_with_configuring_mocks"
        # Same as before...
        mock_api = Mock()  # make a mock for the api
        user = friends.User(api=mock_api)  # Create the user object, using the mock
        # ...but this time, we specify results
        mock_api.friends_ids = [1, 2, 3]
        # We have to be a little fancy with the tweepy mock, because it's
        # a chained call. So we first get a reference to the Cursor() return
        # value, then mock the items() call on that.
        cursor_mock = self.mock_tweepy.Cursor.return_value
        cursor_mock.items.return_value = [4, 5, 6]

        # ACT
        result = user.get_friends_ids("userid")

        # Now notice:
        #   - the result is [4, 5, 6], as we set above
        print result
        #   - the call to tweepy.Cursor() includes the [1, 2, 3] api.friends_ids
        #     that we set above
        print self.mock_tweepy.mock_calls

        # ASSERT
        # Any of these things can be asserted, depending on how flexible we want
        # the code to be:
        expected = [4, 5, 6]
        #   -- check the result directly
        self.assertEqual(result, expected)
        #   -- check that tweepy.Cursor() was called with specific arguments
        self.mock_tweepy.Cursor.assert_called_with([1, 2, 3], user_id='userid')
        #   -- check that tweepy.Cursor() was called with 1 regular and 1
        #      keyword-argument, but with anything as the value
        self.mock_tweepy.Cursor.assert_called_with(ANY, user_id=ANY)
        #   -- check that tweepy.Cursor() was called with anything at all
        assert self.mock_tweepy.Cursor.called
        print "\nYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY\n" # space between tests


# Notice new class, no setup()
class TestFriendsNoSetup(unittest.TestCase):

    def test_example_with_things_going_wrong(self):
        print "test_example_with_things_going_wrong"
        # So why go through all this mocking?  One of the biggest advantages is
        # to test how your code responds to error.  What if tweepy throws a
        # TweepError?  Do you catch it correctly?  Mocks can help you check.

        # We need to use tweepy.TweepError, so we no longer want to mock the module,
        # just the Cursor() call.  Here's a way of doing that just within a
        # single test.
        with patch('friends.tweepy.Cursor') as mock_cursor:
            # Same as before...
            mock_api = Mock()
            user = friends.User(api=mock_api)
            # ...but this time, we make it blow up

            # We need to use the actual tweepy error here.  We can avoid an
            # import by going through the friends namespace:
            mock_cursor.side_effect = friends.tweepy.TweepError("BOOM!")

            # ACT
            # During this call, tweepy.Cursor() will throw an exception.
            result = user.get_friends_ids("userid")

            # ASSERT
            # You can check things:
            # Did you know that None is returned if there's an error?
            self.assertEqual(result, None)
            # You can also check that certain things were printed to stdout
            # or stderr (the 2 most common output streams).  That's a little
            # out of scope, so I won't demo it here.  But it can be done easily.

            print "\nZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\n" # space between tests

            # For comparison, we can demonstrate that other exceptions are
            # let through.
            mock_cursor.side_effect = Exception("BOOM2!")

            # This block will fail if it reaches the end without an exception
            # being thrown.
            with self.assertRaises(Exception):
                user.get_friends_ids("userid")   # Allows exception to go through


if __name__ == '__main__':
    unittest.main()
