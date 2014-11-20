"""
	Score twitter timelines using Naive Bayes classifier.
	A user's score is an aggregate score based on twitter timeline.

	Tutorial: http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
"""

import simplejson as json
import os
import re
import model

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn import cross_validation
from sklearn import metrics


def extract_text(statuses):
    """
    Extract text from a given twitter user's timeline and
    append to list.
    Parameters:
    -----------
    Statuses: the new twitter user's timeline, a python object
    containing status objects.

    Output:
    -------
    List of statuses' text fields.
    """
    text_list = []

    for status in statuses:
        text = status["text"]
        text_list.append(text)

    return text_list


def get_fraction_cons(text_list, label_list):
    """
    Get fraction of training data that is associated with "cons" (conservative)
    label.
    """
    total_length = len(text_list)
    # print "total length", total_length
    cons_list = [label for label in label_list if label == 'cons']
    # print cons_list
    cons_fraction = len([label for label in label_list if label == 'cons'])
    # print "fraction of data that is conservative: ", cons_fraction, " out of ", total_length
    return cons_fraction

def vectorize(text_list, label_list):
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
    makeVector = TfidfVectorizer(analyzer="word", stop_words="english")

    X = makeVector.fit_transform(text_list)
    y = np.array(label_list)

    return X, y

def init_and_train_classifier(X, y, Kfolds):
    """
    Instantiates and trains a classifier.

    Parameters:
    ----------
    Matrix of features and documents
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

        p,r,f1_score,support = metrics.precision_recall_fscore_support(y_test, y_hat)

        # which label's precision does p[1] represent - lib or cons?
        precision.append(p[1])
        recall.append(r[1])

    print 'avg precision:',np.average(precision), '+/-', np.std(precision)
    print 'avg recall:', np.average(recall), '+/-', np.std(recall)
    print 'f1 measure', f1_score

    print "clf: ", clf
    print "cv: ", cv

    return clf

def main():
	TEXT = list()
	LABELS = list()

	data = model.Status.get_all_statuses()
	for status in data:
		TEXT.append(status.text)
		LABELS.append(status.label)

	print TEXT[:10]
	print LABELS[:10]

	get_fraction_cons(TEXT, LABELS)
	X, y = vectorize(TEXT, LABELS)
	init_and_train_classifier(X, y, 3)

if __name__ == "__main__":
	main()