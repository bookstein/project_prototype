
# coding: utf-8

# In[1]:

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

import modelNB


# In[3]:

TEXT = []
LABELS = []

data = modelNB.Status.get_all_statuses()
for status in data:
    TEXT.append(status.text.lower())
    #label 'p' for political
    if status.label == "p":
        LABELS.append("p")
    else:
        LABELS.append("np")
    


# In[4]:

print "TEXT LEN:", len(TEXT)
print "LABELS LEN:", len(LABELS)
print TEXT[1]


# In[5]:

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


# In[6]:

stops = ['http', 'rt']
stops.extend(ENGLISH_STOP_WORDS)


# In[7]:

makeVector = TfidfVectorizer(analyzer="word", stop_words=stops)
print makeVector


# In[8]:

# create vector from raw documents (X)
X = makeVector.fit_transform(TEXT)
print X.shape
# print X

# create numpy array of labels
# numpy arrays = n-dimensional array with collection of items all the same type. Homogenous.
y = np.array(LABELS)
print y.shape


# In[9]:

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


# In[10]:

clf = BernoulliNB()


# In[11]:

clf.fit(X, y)


# In[12]:

Kfolds = 5


# In[13]:

cv = cross_validation.StratifiedKFold(y, Kfolds)


# In[14]:

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


# In[15]:

with open('classifierNB.pkl', 'wb') as fid:
    pickle.dump(clf, fid)


# In[16]:

tweet1 = 'This Veterans Day, join me at #TheConcertForValor, a free event at the #NationalMall in Washington DC https://www.youtube.com/watch?v=U8NtbVL-CKM …'
tweet2 = 'Here is our piece on Iraqi and Afghani translators from last night. Buckle up. http://www.youtube.com/watch?v=QplQL5eAxlY&list=UU3XTzVzaHQEd30rQbuvCtTQ&index=1 …'


# In[17]:

# concatenate tweets to make a 'timeline' -- 
# roughly equivalent to rating each tweet separately and then averaging based on this example data
timeline = [tweet1, tweet2]
sample = makeVector.transform(timeline)


# In[18]:

print sample


# In[20]:

# get classifier from pickle
with open('classifierNB.pkl', 'rb') as fid:
    clf2 = pickle.load(fid)
    
print clf2


# In[21]:

# class prediction
prediction = clf2.predict(sample)
print prediction

# probabilities of belonging to class == SCORE!
probs = clf2.predict_proba(sample)
print probs
print type(probs)


# In[22]:

def average_political_score(probs):
    score = 0
    
    print len(probs)
    
    for prob in probs:
        score += prob.item(1)
            
    # higher probabilities in logistic regression indicate p timeline now
    # ndarray ordered lexigraphically (np before p)
    average_score = score/len(probs)
    print average_score
    
    return average_score


# In[23]:

average_political_score(probs)


# In[24]:

def connect_to_API():
    """
    Create instance of tweepy API class with OAuth keys and tokens.
    """
    # initialize tweepy api object with auth, OAuth
    TWITTER_API_KEY=os.environ.get('TWITTER_API_KEY')
    TWITTER_SECRET_KEY=os.environ.get('TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN=os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_SECRET_TOKEN=os.environ.get('TWITTER_SECRET_TOKEN')

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY, secure=True)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)
    api = tweepy.API(auth, cache=None) #removed wait_on_rate_limit=True, wait_on_rate_limit_notify=True
    return api


# In[25]:

api = connect_to_API()


# In[26]:

def get_timeline(api, uid, count):
    """Get n number of tweets by passing in user id and number of statuses.
        If user has protected tweets, returns [] rather than break the program.
    """
    try:
        feed = tweepy.Cursor(api.user_timeline, id=uid, include_rts=True).items(count)
        # logging.info("\n\n\n", "Get timeline: ", feed, "\n\n\n")
        print "get request timeline"
        return feed

    except tweepy.TweepError as e:
        print e.message[0]["error"]
        return []


# In[27]:

maddow = get_timeline(api, "maddow", 20)


# In[28]:

kimkardashian = get_timeline(api, "KimKardashian", 20)
scalzi = get_timeline(api, "scalzi", 20)


# In[29]:

timeline = []


# In[34]:

for tweet in maddow:
    timeline.append(tweet.text)


# In[35]:

sample = makeVector.transform(timeline)
print sample


# In[36]:

# class prediction
prediction = clf2.predict(sample)
print prediction

# probabilities of belonging to class == SCORE!
probs = clf2.predict_proba(sample)
print probs
print zip(prediction, timeline)


# In[37]:

average_political_score(probs)


# In[104]:




# In[ ]:



