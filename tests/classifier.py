import simplejson as json
import numpy as np
import os
import re
from nltk import NaiveBayesClassifier
import nltk.classify
from nltk import FreqDist
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation


liberal_hashtags = [("p2", "l"), ("p2", "l"), ("p2", "l"), ("dems", "l"), ("obama","l")]
conservative_hashtags = [("tcot", "r"), ("tcot", "r"), ("tcot", "r"), ("teaparty", "r"), ("gop", "r")]


hashtags = []
for (hashtag, affiliation) in liberal_hashtags + conservative_hashtags:
	hashtags.append((hashtag, affiliation))

# print hashtags


def get_word_features(hashtags):
    hashtags = FreqDist(hashtags)
    print "HASHTAGS", hashtags.most_common(2)
    print "FREQUENCY", hashtags["p2"]
    features = hashtags.keys()
    return features

word_features = get_word_features(hashtags)
# print word_features
