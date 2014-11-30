import json
import pickle

import numpy as np
import tweepy

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn import cross_validation
from sklearn import metrics

import politwit.model as model

ENGLISH_STOP_WORDS = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fify", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"]


classifier = LogisticRegression()
Kfolds = 5
OUTPUT_FILE = ""

def label_data():
    TEXT = []
    LABELS = []

    data = model.Status.get_all_statuses()
    for status in data:
        TEXT.append(status.text.lower())
        #label 'p' for political
        if status.label == "libs" or status.label == "cons":
            LABELS.append("p")
        else:
            LABELS.append("np")

    print len(LABELS), len(TEXT)
    return TEXT, LABELS

def makeVector():
    stopwords = ["http", "rt"]
    stopwords.extend(ENGLISH_STOP_WORDS)

    return TfidfVectorizer(analyzer="word", stop_words=stopwords)

def transform_documents(, vectorizer):
    """
    Transform given documents into vectors of features, with matching vector of labels.

    Paramters:
    ----------
    Vectorizer

    Output:
    -------
    X (matrix of documents and features)
    y (single-dimensional matrix of labels)
    """
    # create vector from raw documents (X)
    X = vectorizer.fit_transform(TEXT)
    print X.shape

    # create numpy array of labels
    y = np.array(LABELS)
    print y.shape

    return X, y

def get_fraction_np():
    """
    Get fraction of training data that is associated with "np" (nonpolitical) label.
    """
    # get number of nonpolitical
    np_list = [label for label in LABELS if label == 'np']
    np_fraction = float(len(np_list))/float(len(TEXT))

    print np_fraction

    return np_fraction

def train(clf):
    """
    Train and cross-validate classifier by dividing training set into K-fold number of test and training sets.

    Parameters:
    -----------
    Sci-kit learn classifier.

    Output:
    -------
    Trained classifier.
    Precision and recall metrics printed to console.
    """
    cv = cross_validation.StratifiedKFold(y, Kfolds)
    precision = []
    recall = []

    for train, test in cv:
        X_train = X[train]
        X_test = X[test]
        y_train = y[train]
        y_test = y[test]

        # train classifier
        clf.fit(X_train, y_train)

        y_hat = clf.predict(X_test)

        # get values for precision, recall, f1_score, support
        p,r,f1_score,s = metrics.precision_recall_fscore_support(y_test, y_hat)

        precision.append(p[1])
        recall.append(r[1])

    print 'avg precision:',np.average(precision), '+/-', np.std(precision)
    print 'avg recall:', np.average(recall), '+/-', np.std(recall)
    print 'f1 measure', f1_score

    print "clf: ", clf
    print "cv: ", cv

    return clf

def main():

    """
    Produces a trained and tested classifier, exports to pickle.
    Used for "scoring" user timelines by "political" or "nonpolitical" class probability.

    Parameters:
    ----------
    Classifier model (e.g. LogisticRegression)
    Filename for pickling trained classifer

    Output:
    ------
    Trained classifer, pickled to specified file.

    """
    TEXT, LABELS = label_data()
    vectorizer = makeVector()

    X, y = transform_documents(vectorizer)
    clf = train(classifier)

    with open(OUTPUT_FILE, 'wb') as fid:
        pickle.dump(clf, fid)

    print "pickled to ", filename

if __name__ == "__main__":
	main()
