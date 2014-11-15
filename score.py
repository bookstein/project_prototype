"""
	Score tweet using this algorithm.
	A user's score is an aggregate score based on individual tweet scores.
	Compare link to entry in database, throw out if no corresponding data.
"""

import simplejson as json
import numpy as np
import os
import re
from nltk import NaiveBayesClassifier
import nltk.classify
from nltk import FreqDist
from nltk.tokenize import wordpunct_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation

def get_json_data(filename):
	"""
	Input filename containing array of JSON-format statuses.
	Output is list of dictionaries.
	"""
	f = open(filename)

	# decodes all file data from json
	statuses_data = json.load(f)
	return statuses_data

def parse_statuses(statuses):
	"""Given decoded json statuses for a given user, gets text, hashtags, and links from all statuses.

	Parameters:
	----------
	Output from get_json_data

	Output:
	-------
	Arrays containing tweet text, hashtags, urls as strings.
	"""
	text_list = []
	hashtags_list = []
	urls_list = []

	for status in statuses:

		text = status["text"]
		entities = status["entities"]

		for i in range(len(entities["urls"])):
			# appends url as it exists in the tweet text
			url = entities["urls"][i]["url"]
			urls_list.append(url)
			match = re.search(url, text)
			if match:
				text = re.sub(r"(?:\@|https?\://)\S+", " ", text)
				print "TEXT AFTER MATCH ", text

		text_list.append(text)
		hashtags_list.append(entities["hashtags"])


	return text_list, hashtags_list, urls_list


def word_count(status_text, affiliation="liberal"):
	"""
	Iterates through input user statuses (twitter feed) to calculate word counts.

	Parameters:
	-----------
	Text of a given user's statuses, as a list of strings.
	Political affiliation of user (either liberal or conservative)


	Outputs:
	--------
	Dictionary with word counts (lowercase word, frequency).
	This can be used to get scores of a seed group of known political agents.


	"""
	keywords = {
		"liberal" : {},
		"conservative" : {}
	}

	hashtags = {
		"liberal": {},
		"conservative" : {}
	}

	d = keywords[affiliation]
	h = hashtags[affiliation]

	for text in status_text:
		text = set(word_tokenize(text.lower()))
		print text



	# 	for word in words:
	# 		if word[0] == "#":
	# 			hashtag = word[1:]
	# 			print hashtag
	# 			h[hashtag] = h.get(hashtag, 0) + 1
	# 		else:
	# 			d[word] = d.get(word, 0) + 1

	# print h
	# return d, h


def get_words(text, stopwords = []):
	"""
	Given words:
	Remove punctuation and words smaller than 2 letters, make all words lowercase.

	Inputs:
	-------
	Text from all statuses. (?)

	Outputs:
	--------
	Text made lowercase, without punctuation, ready to split into tokens.
	"""
	for single_tweet in text:
		print "SINGLE TWEET ", single_tweet

		# tokenize a string to split off punctuation other than periods
		text_words = set(wordpunct_tokenize(single_tweet))
		print "WORDPUNCT WORDS", text_words

		# Remove stopwords
		text_words = text_words.difference(stopwords)
		print "AFTER REMOVING STOPWORDS", text_words, "\n\n"

	# return text_words


def main():
	# pass
	data = get_json_data("./json/maddow/self.json")
	text, hashtags, urls = parse_statuses(data)
	# processed_text = process_text(text, stopwords)
	# print processed_text
	# print get_words(text)


if __name__ == "__main__":
	main()


