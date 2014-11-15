"""
	Score tweet using this algorithm.
	A user's score is an aggregate score based on individual tweet scores.
	Compare link to entry in database, throw out if no corresponding data.
"""

import simplejson as json
import numpy as np
import os
import re
from collections import defaultdict
from string import punctuation

from nltk import NaiveBayesClassifier
import nltk.classify
from nltk import FreqDist
from nltk.tokenize import wordpunct_tokenize, word_tokenize
from nltk.corpus import stopwords

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

def extract_hashtags(statuses, hashtag_set):
	"""
	Extract hashtags from a given twitter user's timeline.

	Parameters:
	-----------
	Hashtag_set is the set of hashtags to which new hashtags will be added.
	Statuses refers to the new twitter user timeline, a python object containing status objects.

	Output:
	-------
	Side-effect function, modifying hashtag_set.
	"""
	for status in statuses:
		new_hashtags = status["entities"]["hashtags"]
		# will skip over empty lists - no obj inside
		for hashtag_obj in new_hashtags:
			hashtag_set.add(hashtag_obj["text"])



	return hashtag_set



def get_hashtags_from_tweets(statuses):
	"""
	Return list of hashtags used throughout user timeline.

	Given decoded json statuses for a given user, parses status, appends (hashtags, label) to a list of hashtags.

	Parameters:
	----------
	Statuses: list of twitter status updates for 1 user. Each element is a JSON object from Twitter API converted to a Python object.

	Output:
	-------
	List of all hashtags from user timeline.
	"""
	all_hashtags = []

	for status in statuses:
		new_hashtags = status["entities"]["hashtags"]
		for hashtag_obj in new_hashtags:
			hashtag = hashtag_obj["text"]
			all_hashtags.append(hashtag)

	print "ALL HASHTAGS", all_hashtags
	return all_hashtags


def get_features(hashtags):
	"""
	Order hashtags by frequency.

	Parameters:
	----------
	List of all hashtags.

	Output:
	------
	Hashtag_features, a set of hashtags listed in order of frequency of appearance.
	"""
	hashtags_dist = FreqDist(hashtags)
	hashtag_features = hashtags_dist.keys()
	return hashtag_features

def extract_features(hashtags, HASHTAGS):
	"""
	Given a list of hashtags, create dictionary of (hashtag: True) pairs indicating
	presence of absence of hashtag

	Parameters:
	----------
	Statuses as a python object.
	"""

	hashtag_set = set(hashtags)
	features = {}
	# look in global collection of hashtags for matches
	for hashtag in HASHTAGS:
		print hashtag
		features['contains(%s)'% hashtag] = (hashtag in hashtag_set)
	print features
	return features



# TODO: clean up or rewrite code below this line - replace with Laurent Luce tutorial



def features_from_hashtags(hashtags):
	"""Given a list of hashtags, assign a political affiliation.
	Return a dictionary with hashtags and frequency (FreqDist).
	"""
	# all_hashtags = []

	# for hashtag_list in hashtags:
	# 	all_hashtags.extend(hashtag_list)

	# features = all_hashtags
	hashtags = FreqDist(hashtags)
	features = hashtags.keys()
	print features
	return features

	# features_list = []
	# feature_set = defaultdict(list)

	for hashtag_collection in hashtags:
		# tuple contains (list of hashtags, political label)
		features_list.append((hashtag_collection, label))
		for hashtag in hashtag_collection:
			feature_set[hashtag] = True
			print hashtag

	# print "FEATURE SET ", feature_set
	# return feature_set




def make_training_test_sets(feature_extractor):
	"""Make training sets of data by adding a label of "lib" or "cons" to data.
	Train algorithm using training sets."""

	train_liberal = feature_extractor(get_hashtags(train_liberal_tweets), label="lib")
	train_conservative = feature_extractor(get_hashtags(train_conservative_tweets), label="cons")

	train_set = train_liberal + train_conservative

	test_liberal = feature_extractor(get_hashtags(test_liberal_tweets), "lib")
	test_conservative = feature_extractor(get_hashtags(test_conservative_tweets), "cons")

	return train_set, test_liberal, test_conservative

def check_classifier(feature_extractor):
	"""Trains classifier on the training data (lib and cons), checks accuracy on the test data."""
	#Make the training and testing sets.
	train_set, test_liberal, test_conservative = make_training_test_sets(feature_extractor)

	print "TRAINING SET ", train_set
	print "TEST LIB ", test_liberal
	print "TEST CON ", test_conservative

	#Train the classifer using the training set
	classifier = NaiveBayesClassifier.train(train_set)

	# How accurate is the classifier on the test sets?
	# print ('Test Lib accuracy: {0:.2f}%'.format(100 * nltk.classify.accuracy(classifier, test_liberal)))
	# print ('Test Cons accuracy: {0:.2f}%'.format(100 * nltk.classify.accuracy(classifier, test_conservative)))

 #    # Show the top 20 informative features
	# print classifier.show_most_informative_features(2)



# parsed_liberal_tweets = get_hashtags(train_liberal_tweets)

def main():
	lib_tweets = get_json_data(LIBERAL_TWEETS_PATH)
	cons_tweets = get_json_data(CONSERVATIVE_TWEETS_PATH)

	HASHTAGS = set()
	extract_hashtags(lib_tweets, HASHTAGS)
	# label can come last!!
	classifier = (list(HASHTAGS), "libs")
	# print hashtags
	print classifier
	# loop through timelines, add to hashtags


# #equivalent of pos_tweets
# LIB_HASHTAGS = get_hashtags(LIBERAL_TWEETS, "lib")
# #equivalent of neg_tweets
# CONS_HASHTAGS = get_hashtags(CONSERVATIVE_TWEETS, "cons")

# create a single list of tuples (equivalent of "tweets"), labeled
# HASHTAGS = []
# for (hashtag, affiliation) in LIB_HASHTAGS + CONS_HASHTAGS:
# 	HASHTAGS.append((hashtag, affiliation))

# HASHTAGS is an unlabeled list when using get_all_hashtags to create
# HASHTAGS = (get_all_hashtags(LIB_HASHTAGS) + get_all_hashtags(CONS_HASHTAGS))
# print HASHTAGS
# if I set HASHTAGS = LIB_HASHTAGS + CONS_HASHTAGS, then I get an error from extract_features saying it cannot hash a list!!!

# test = extract_features(("tomcat", "p2", "CookerPot"))
# print test

# apply features to the classifier, passing into it the labeled data
# WHAT IS THIS ACTUALLY DOING?
# training set contains labeled feature sets.
# so why does mine only contain liberal hashtags? something about the way I set this up? HASHTAGS was supposed to combine both the lists.
# training_set = nltk.classify.apply_features(extract_features, LIB_HASHTAGS)

if __name__ == "__main__":
	main()