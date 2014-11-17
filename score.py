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

	#TODO: get data from database, not json, for training data
	This affects extract_hashtags function as well.

	"""
	with open(filename) as f:
		# decodes all file data from json
		statuses_data = json.load(f)
		return statuses_data

def extract_hashtags(statuses, hashtag_list, label_list, label):
    """
    Extract hashtags from a given twitter user's timeline and
    append them to an existing list.
    Add corresponding label to a list of labels.
    Parameters:
    -----------
    Hashtag_list is the list of hashtags to which new hashtags will be added.
    Statuses refers to the new twitter user timeline, a python object
    containing status objects.
    Label_list is the corresponding list of labels for hashtags added in batches
    to hashtag_list.
    Label is the label that is appended to label_list (either "lib" or "cons")
    Output:
    -------
    Side-effect, modifying hashtag_list and label_list. Does not return a value.
    """
    for status in statuses:
        new_hashtags = status["entities"]["hashtags"]
        # will skip over empty lists - no obj inside
        for hashtag_obj in new_hashtags:
            hashtag_list.append(hashtag_obj["text"])
            label_list.append(label)



def get_fraction_cons(hashtag_list, label_list):
    """
    Get fraction of training data that is associated with "cons" (conservative)
    label.
    """
    total_length = len(hashtag_list)
    print "total length", total_length
    cons_list = [label for label in label_list if label == 'cons']
    print cons_list
    cons_fraction = len([label for label in label_list if label == 'cons'])
    print "fraction of data that is conservative: ", cons_fraction, " out of ", total_length
    return cons_fraction

def vectorize(hashtag_list, label_list):
    """
    "Vectorize" hashtag list and labels list into a matrix of token counts.

    Parameters:
    -----------
    List of all hashtags in dataset as strings, list of all associated labels
    as strings.

    Output:
    -------
    Matrix of token counts (hashtags, by occurrence)

    Note: CountVectorizer can also look at ngrams - useful for examining entire
    tweet text instead of hashtags.
    """
    makeVector = CountVectorizer()

    X = makeVector.fit_transform(hashtag_list)
    y = np.array(label_list)

    return X, y

def init_and_train_classifier(X, y, Kfolds):
    """
    Instantiates and trains a classifier.

    Parameters:
    ----------
    List of labels (as numpy array)
    Number of stratified folds into which to divide all labelled data.

    Output:
    -------
    Trained classifier
    """

    clf = BernoulliNB()

    cv = cross_validation.StratifiedKFold(y, Kfolds)

    precision = []
    recall = []

    for train, test in cv:
        X_train = X[train]
        X_test = X[test]
        y_train = y[train]
        y_test = y[test]

        clf.fit(X_train, y_train)

        y_hat = clf.predict(X_test)

    # TODO: double-check that I understand r and p (why are they appended to array?)!
        p,r,f1_score,support = metrics.precision_recall_fscore_support(y_test, y_hat)
        precision.append(p[1])
        recall.append(r[1])

    print 'precision:',np.average(precision), '+/-', np.std(precision)
    print 'recall:', np.average(recall), '+/-', np.std(recall)


    print "clf: ", clf
    print "cv: ", cv


    return clf



def main():
	HASHTAGS = list()
	LABELS = list()

	# extract_hashtags: statuses, hashtag_list, label_list, label

	lib_tweets = get_json_data(LIBERAL_TWEETS_PATH)
	cons_tweets = get_json_data(CONSERVATIVE_TWEETS_PATH)

	for i in range(10):
		extract_hashtags(lib_tweets, HASHTAGS, LABELS, "lib")
		extract_hashtags(cons_tweets, HASHTAGS, LABELS, "cons")

	# loop through timelines, add to HASHTAGS

	get_fraction_cons(HASHTAGS, LABELS)
	X, y = vectorize(HASHTAGS, LABELS)
	init_and_train_classifier(X, y, 3)


if __name__ == "__main__":
	main()