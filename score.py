"""
	Score twitter timelines using Naive Bayes classifier.
	A user's score is an aggregate score based on twitter timeline.

	Tutorial: http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
"""

import simplejson as json
import os
import re

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn import cross_validation
from sklearn import metrics

LIBERAL_TWEETS_PATH = "./json/maddow/self.json"
CONSERVATIVE_TWEETS_PATH = "./json/rushlimbaugh/self.json"


def get_json_data(filename):
	"""
	Input filename containing array of JSON-format statuses.
	Output is list of dictionaries representing Twitter
	timeline from one user.
	"""
	with open(filename) as f:
		# decodes all file data from json
		statuses_data = json.load(f)
		return statuses_data

def extract_hashtags(statuses, hashtag_list):
	"""
	Extract hashtags from a given twitter user's timeline and
	append them to an existing list.

	Parameters:
	-----------
	Hashtag_list is the list of hashtags to which new hashtags will be added.
	Statuses refers to the new twitter user timeline, a python object
	containing status objects.

	Output:
	-------
	Side-effect, modifying hashtag_list. Does not return a value.
	"""
	for status in statuses:
		new_hashtags = status["entities"]["hashtags"]
		# will skip over empty lists - no obj inside
		for hashtag_obj in new_hashtags:
			hashtag_list.append(hashtag_obj["text"])

	# return hashtag_list

def get_unique_hashtags(labeled_hashtags):
	"""
	Take hashtags from list of labeled tuples and create list of unlabeled hashtags.

	Parameters:
	------------
	A list of tuples containing hashtags and their associated labels

	Output:
	-------
	A list of unlabeled hashtags.
	"""

	all_hashtags = []
	for (hashtags, label) in labeled_hashtags:
		all_hashtags.extend(hashtags)
	return all_hashtags

def get_hashtags_as_features(unlabeled_hashtags):
	"""
	Order hashtags by frequency and output a list of dictionary keys in order of
	frequency.

	Parameters:
	----------
	List of all hashtags, both liberal and conservative, unlabelled.

	Output:
	------
	Unique list of hashtags, hashtag_features, which are the keys to a dictionary
	created by FreqDist.
	"""
	hashtags_dist = FreqDist(unlabeled_hashtags)
	hashtag_features = hashtags_dist.keys()
	return hashtag_features

def extract_features(hashtags, unlabeled_hashtags):
	"""
	Create dictionary of (hashtag: True) pairs indicating
	presence or absence of hashtag

	Parameters:
	----------
	Specific list of hashtags. ("document")

	Output:
	-------
	Dictionary of true-false values showing which features were present in the
	given list of hashtags.
	"""

	hashtag_set = set(hashtags)
	features = {}
	# look in global collection of hashtags for matches
	for hashtag in unlabeled_hashtags:
		print hashtag
		features['contains(%s)'% hashtag] = (hashtag in hashtag_set)
	print features
	return features




# TODO: make training sets and test sets, check classifier




def main():
	lib_tweets = get_json_data(LIBERAL_TWEETS_PATH)
	LIB_HASHTAGS = list()
	# adds to HASHTAGS list
	extract_hashtags(lib_tweets, LIB_HASHTAGS)
	# label can come last!!
	classifier1 = ((LIB_HASHTAGS, "libs"))
	# print classifier1

	cons_tweets = get_json_data(CONSERVATIVE_TWEETS_PATH)
	CONS_HASHTAGS = list()
	extract_hashtags(cons_tweets, CONS_HASHTAGS)
	classifier2 = ((CONS_HASHTAGS, "cons"))
	# print classifier2

	HASHTAGS = list()
	HASHTAGS.extend((classifier1, classifier2))
	print HASHTAGS

	unlabeled = get_unique_hashtags(HASHTAGS)
	features = get_hashtags_as_features(unlabeled)
	hits = extract_features(["Maddow", "tcot", "CookerPot"], features)
	print hits

	# loop through timelines, add to HASHTAGS


if __name__ == "__main__":
	main()