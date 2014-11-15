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






# TODO: clean up or rewrite code below this line - replace with Laurent Luce tutorial




# def make_training_test_sets(feature_extractor):
# 	"""Make training sets of data by adding a label of "lib" or "cons" to data.
# 	Train algorithm using training sets."""

# 	train_liberal = feature_extractor(get_hashtags(train_liberal_tweets), label="lib")
# 	train_conservative = feature_extractor(get_hashtags(train_conservative_tweets), label="cons")

# 	train_set = train_liberal + train_conservative

# 	test_liberal = feature_extractor(get_hashtags(test_liberal_tweets), "lib")
# 	test_conservative = feature_extractor(get_hashtags(test_conservative_tweets), "cons")

# 	return train_set, test_liberal, test_conservative

# def check_classifier(feature_extractor):
# 	"""Trains classifier on the training data (lib and cons), checks accuracy on the test data."""
# 	#Make the training and testing sets.
# 	train_set, test_liberal, test_conservative = make_training_test_sets(feature_extractor)

# 	print "TRAINING SET ", train_set
# 	print "TEST LIB ", test_liberal
# 	print "TEST CON ", test_conservative

# 	#Train the classifer using the training set
# 	classifier = NaiveBayesClassifier.train(train_set)

# 	# How accurate is the classifier on the test sets?
# 	# print ('Test Lib accuracy: {0:.2f}%'.format(100 * nltk.classify.accuracy(classifier, test_liberal)))
# 	# print ('Test Cons accuracy: {0:.2f}%'.format(100 * nltk.classify.accuracy(classifier, test_conservative)))

#  #    # Show the top 20 informative features
# 	# print classifier.show_most_informative_features(2)



# parsed_liberal_tweets = get_hashtags(train_liberal_tweets)
def storage():
	r = get_hashtags_from_tweets(lib)
	dist = get_features(r)
	feat = extract_features(["p2", "tcot", "Maddow"], r)
	training_set = nltk.classify.apply_features(extract_features, HASHTAGS, r)
	print training_set

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