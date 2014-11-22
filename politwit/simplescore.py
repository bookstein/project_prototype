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
		"""
		political_count = 0
		total_num_hashtags = 0

		for hashtag in self.hashtags_dict:
			total_num_hashtags += self.hashtags_dict[hashtag]

		for hashtag in matches:
			political_count += matches[hashtag]

		score = float(political_count)/float(total_num_hashtags)

		return score


def main():
	h = {"tcot": 5, "banana": 10}
	m = matching_hashtags(h)
	s = score_by_hashtags(m, h)
	print s

if __name__ == "__main__":
	main()