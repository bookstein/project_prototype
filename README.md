#Politicization on Twitter#

A project for Hackbright Academy, Fall 2014.

Using data from Twitter's Search and REST API, as well as scikit-learn's Bernoulli Naive Bayes classifer, visualize the recent intensity of political activity within any Twitter user's friend group. An interactive bubble chart shows the user's 50 most influential friends, as measured by number of followers.

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

Search for any Twitter user by entering a Twitter handle into the search field.

The result is a "politicalness" score for each of the top 50 most influential friends (people that user follows). The score is a fraction between 0 and 1 -- determined by averaging probabilities given by a Naive Bayes classifier that any given tweet is political. 20 tweets are collected per friend, so the politicalness score may be only a measure of recent political dialogue.

The data is rendered in d3 as a bubble chart, with each bubble representing a Twitter account. Bubbles' opacity varies with the person's politicalness score -- dark bubbles are more political, light bubbles less so. Bubble radii reflect the number of followers.

![ScreenShot](/static/images/scrn_cap3.png "On hover")

Bubbles can be hovered over for more information, or clicked on to reveal the user's 3 most recent tweets.

![ScreenShot](/static/images/scrn_cap2.png "On click")

The Naive Bayes classifier used for generating politicalness scores tends to overpredict political content, probably because the training data is not diverse enough and does not reflect the true proportion of political content on Twitter.

Previously I had used a simple hashtag counter to score users' politicalness, which counted the number of hashtags in a user's timeline and returned a ratio of political to total hashtags.

My training data consists of 60,000 tweets harvested in late November 2014 by querying for specific political and nonpolitical hashtags.

Before deciding on Naive Bayes, I compared its performance to a Logistic Regression algorithm. Both are available in scikit-learn.

    Metric| Bernoulli Naive Bayes  | Logistic Regression
    ------|------------- | -------------
 Precision| 87%          |  76%
    Recall| 88%          |  94%


##Moving forward:##

In broad strokes, here's what I plan to do:

 - Increase the precision of my classifier, both by tuning it, by improving training data, and by testing other classifiers (i.e., Multinomial Bayes, K-near neighbors, SVM) for better performance.

 - Visualize liberal-conservative political leanings on Twitter, to investigate on a case-by-case basis when users have put themselves in a political echo chamber ("homophily") versus in conversation with politically diverse users.

 - Enable login with OAuth (currently using app auth)

 - Recommend diverse Twitter accounts that are either highly similar or highly different, politically, from the current user.

 - Reduce the number of API calls with memcache.

 - Continuously update the visualization, rather than wait for all tweets to be processed (the bottleneck is the Twitter api; getting 20 tweets for 50 friends can take up to 25 seconds altogether!)

 - Write tests using Python's unittest or nosetest

 - Handle errors gracefully, beyond a simple flash message -- in particular errors caused by hitting the Twitter API rate limit


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
