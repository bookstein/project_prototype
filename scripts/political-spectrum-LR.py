
# coding: utf-8

# In[24]:

import simplejson as json
import os
import string
import pickle

import numpy as np
import tweepy

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn import cross_validation
from sklearn import metrics

import model


# In[25]:

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
    


# In[26]:

print "TEXT LEN:", len(TEXT)
print "LABELS LEN:", len(LABELS)
print TEXT[1]


# In[27]:

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


# In[28]:

stops = ['http', 'rt']
stops.extend(ENGLISH_STOP_WORDS)


# In[29]:

makeVector = TfidfVectorizer(analyzer="word", stop_words=stops)
print makeVector


# In[30]:

# create vector from raw documents (X)
X = makeVector.fit_transform(TEXT)
print X.shape
# print X

# create numpy array of labels
# numpy arrays = n-dimensional array with collection of items all the same type. Homogenous.
y = np.array(LABELS)
print y.shape


# In[31]:

def get_fraction_np(text_list, label_list):
    """
    Get fraction of training data that is associated with "np" (nonpolitical)
    label.
    """
    # get number of nonpolitical
    np_list = [label for label in label_list if label == 'np']
    
#     print len(text_list)
#     print len(np_list)
    
    return float(len(np_list))/float(len(text_list))

print get_fraction_np(TEXT, LABELS)


# In[38]:

clf = LogisticRegression()


# In[39]:

clf.fit(X, y)
# train classifier to recognize all tweets as 'political' (single label)


# In[40]:

Kfolds = 5


# In[41]:

cv = cross_validation.StratifiedKFold(y, Kfolds)


# In[42]:

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

    precision.append(p[1])
    recall.append(r[1])

print 'avg precision:',np.average(precision), '+/-', np.std(precision)
print 'avg recall:', np.average(recall), '+/-', np.std(recall)
print 'f1 measure', f1_score

print "clf: ", clf
print "cv: ", cv


# In[43]:

with open('classifierLR.pkl', 'wb') as fid:
    pickle.dump(clf, fid)


# In[44]:

tweet1 = 'This Veterans Day, join me at #TheConcertForValor, a free event at the #NationalMall in Washington DC https://www.youtube.com/watch?v=U8NtbVL-CKM …'
tweet2 = 'Here is our piece on Iraqi and Afghani translators from last night. Buckle up. http://www.youtube.com/watch?v=QplQL5eAxlY&list=UU3XTzVzaHQEd30rQbuvCtTQ&index=1 …'


# In[45]:

# concatenate tweets to make a 'timeline' -- 
# roughly equivalent to rating each tweet separately and then averaging based on this example data
timeline = [tweet1 + tweet2]
sample = makeVector.transform(timeline)


# In[46]:

print sample


# In[47]:

# get classifier from pickle
with open('classifierLR.pkl', 'rb') as fid:
    clf2 = pickle.load(fid)


# In[48]:

# class prediction
prediction = clf2.predict(sample)
print prediction

# probabilities of belonging to class == SCORE!
probs = clf2.predict_proba(sample)
print probs


# In[102]:

# print clf.predict_log_proba(makeVector.transform([tweet1]))
# print clf.predict_log_proba(makeVector.transform([tweet2]))


# In[23]:

#feature count


# In[20]:

#log probs


# In[19]:

#list of features (words)


# In[21]:

# sorted(zip(probs,features), reverse=True)[:10]
# zip together features and their probabilities, sort in reverse order (descending)


# In[22]:

# zip together feature log probs with NONPOLITICAL features, in reverse order (descending)
# np_features = sorted(zip(clf.feature_log_prob_[0],features), key=lambda f: f[0], reverse=True)[:10]
# zip together feature log probs with POLITICAL features
# p_features = sorted(zip(clf.feature_log_prob_[1],features), key=lambda f: f[0], reverse=True)[:10]


# In[ ]:



