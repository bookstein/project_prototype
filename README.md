#Politicization on Twitter#

A project for Hackbright Academy, Fall 2014.

Using data from Twitter's Search and REST API, I classify any user's political activity with scikit-learn's Bernoulli Naive Bayesian classifer and visualize the politicalness of the top 50 friends (ranked by number of followers) with D3.

##Main stack/technology##

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

A user can search for any Twitter user's friend group politicization by entering a Twitter handle into the search field.

Flask returns a JSON object containing the top 50 most influential friends of that person, as ranked by number of followers, as well as a "politicalness" score between 0 and 1 -- an average of probabilities given by a Naive Bayes classifier that each tweet is political. Only 20 tweets are collected per friend, so politicalness may be only a measure of recent political dialog.

Finally, the data is rendered in d3 as a flattened hierarchy with a pack layout. Bubbles' opacity varies with the person's politicalness score -- dark bubbles are more political, light bubbles less so.

![ScreenShot](/static/images/scrn_cap3.png "On hover")

Bubbles can be hovered over for more information, or clicked on to reveal the user's 3 most recent tweets.

![ScreenShot](/static/images/scrn_cap2.png "On click")

The Naive Bayes classifier used for generating politicalness scores has a precision of about 87% and recall of 88%. It tends to overpredict political content.

Previously I had used a simple hashtag counter to score users' politicalness, which counted the number of hashtags in a user's timeline and returned a ratio of political to total hashtags.

My training data consists of 60,000 tweets harvested in late November 2014 by querying for specific political and nonpolitical hashtags.

Before deciding on Naive Bayes, I compared its performance to a Logistic Regression algorithm. Both are available in scikit-learn.

    Metric| Bernoulli Naive Bayes  | Logistic Regression
    ------|------------- | -------------
 Precision| 87%          |  88%
    Recall| 76%          |  94%


##Moving forward:##
 -Increase the precision of my classifier, both by tuning it, by improving training data, and by testing other classifiers (i.e., K-near neighbors, SVM).

 -Visualize political leanings on Twitter, to investigate on a case-by-case basis when users have put themselves in a political echo chamber ("homophily") versus in conversation with politically diverse users. This will be accomplished by classifying tweets as liberal/nonliberal and conservative/nonconservative.

 -Enable login with OAuth

 -Recommend diverse Twitter accounts that are either highly similar or highly different, politically, from the current user.


## Cloning Instructions ##

> ### NOTE: you will need your own Twitter tokens and access keys to run this app.###

    # clone repository into a local directory
    git clone https://github.com/bookstein/project_prototype.git

    # create a virtual environment (here named 'env') and activate, so that dependencies will be installed only in this environment and not globally
    virtualenv env
    source env/bin/activate

    # export Twitter tokens and keys to shell by adding these lines in env/bin/activate
    export TWITTER_API_KEY="..."
    export TWITTER_SECRET_KEY="..."
    export TWITTER_ACCESS_TOKEN="..."
    export TWITTER_SECRET_TOKEN="..."

    # run this command on the command line to install dependencies.
    # make sure you're in your virtual environment!
    pip install -r requirements.txt

    # run flask_server.py on the command line to start the app
    python flask_server.py

Now visit localhost:5000 in your browser and enjoy!
