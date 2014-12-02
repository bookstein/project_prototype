#Politicization on Twitter#

A project for Hackbright Academy, Fall 2014.

Using data from Twitter's Search and REST API, I classify any user's political activity with scikit-learn's Bernoulli Naive Bayesian classifer and visualize the politicalness of the top 50 friends (ranked by number of followers) with D3.

##Stack/technology##

_backend_:

    -Python Flask

    -scikit-learn

    -SQLAlchemy, sqlite3

_frontend_:

    -d3

    -Foundation/SASS

    -jQuery



##Current project state##

![ScreenShot](/static/images/scrn_cap1.png "Landing Page")

The Naive Bayes classifier has a precision of about 87% and recall of 88%, which I chose over a Logistic Regression classifier; despite good recall, LR precision was much lower.

Previously I had used a simple hashtag counter to score users' politicalness, which counted the number of hashtags in a user's timeline and returned a ratio of political to total hashtags.

My training data consists of 60,000 tweets harvested in late November 2014 by querying for specific political and nonpolitical hashtags.

    Metric| Bernoulli Naive Bayes  | Logistic Regression
    ------|------------- | -------------
 Precision| 87%          |  88%
    Recall| 76%          |  94%

![ScreenShot](/static/images/scrn_cap3.png "On hover")

![ScreenShot](/static/images/scrn_cap2.png "On click")

##Moving forward:##
 -Increase the precision of my classifier, both by tuning it, by improving training data, and by testing other classifiers (i.e., K-near neighbors, SVM).

 -Visualize political leanings on Twitter, to investigate on a case-by-case basis when users have put themselves in a political echo chamber ("homophily") versus in conversation with politically diverse users. This will be accomplished by classifying tweets as liberal/nonliberal and conservative/nonconservative.

 -Enable login with OAuth

 -Recommend diverse Twitter accounts that are either highly similar or highly different, politically, from the current user.


## Cloning Instructions ##

### NOTE: you will need your own Twitter tokens and access keys to run this app.###

    # clone repository into local directory
    git clone ...

    # create a virtual environment and activate to keep installations local
    virtualenv env
    source env/bin/activate

    # export Twitter tokens and keys to shell in env/bin/activate
    export TWITTER_API_KEY="..."
    export TWITTER_SECRET_KEY="..."
    export TWITTER_ACCESS_TOKEN="..."
    export TWITTER_SECRET_TOKEN="..."

    # run this command on the command line to install dependencies
    pip install -r requirements.txt

    # run flask_server.py on the command line to start the app
    python flask_server.py

Now visit localhost:5000 in your browser and enjoy!
