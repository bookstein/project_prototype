"""A dummy module for scoring users."""

import model

class Score(object):

	hashtags_dict = {}
	matches = {}
	score = 0

	def __init__(self, hashtags_dict):
		self.hashtags_dict = hashtags_dict
		self.matches = self.matching_hashtags()
		self.score = self.score_by_hashtags(self.matches)

	def matching_hashtags(self):
		"""
		Create dictionary of all political hashtags, incrementing count by user's
		political hashtags.

		Parameters:
		-----------
		Hashtags_dict is a dictionary of all user's hashtags. Hashtag value is count.

		Output:
		-------
		Dictionary of all political hashtags, where all non-used hashtags have value 0
		and political hashtags used by user show the number of times used.
		"""
		matches = {}

		political_hashtags = model.Hashtag.get_all_political_hashtags()

		for hashtag in political_hashtags:
			matches[hashtag] = self.hashtags_dict.get(hashtag, 0)

		return matches

	def score_by_hashtags(self, matches):
		"""
		Calculate score given matching hashtags.

		Parameters:
		-----------
		Dictionary from output of matching_hashtags - showing all political hashtags, with matching political hashtags counted.

		Output:
		-------
		A score based on percentage of political hashtags out of all hashtags used.
		"""
		political_count = sum(matches.itervalues())
		total_num_hashtags = sum(self.hashtags_dict.itervalues())

		if total_num_hashtags > 0:
			score = float(political_count)/float(total_num_hashtags)
			return score

		else:
			return 0


def main():
	hashtags_dict = {"tcot": 5, "banana": 10}
	s = Score(hashtags_dict)
	print s.score

if __name__ == "__main__":
	main()
