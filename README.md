#Politicization on Twitter#

A project for Hackbright Academy, Fall 2014.

Using data from Twitter's Search and REST API, as well as a Bernoulli Naive Bayes classifer, visualize the intensity of political activity within any Twitter user's friend group in an interactive bubble chart.

##Stack/technology##

_backend_:

    -Python, Flask

    -scikit-learn machine learning library

    -SQLAlchemy, sqlite3

_frontend_:

    -D3

    -Foundation (framework) + SASS

    -jQuery/Javascript

##About the project##

Galvanized by low voter turnout in the 2014 midterm elections, and inspired by my experience with (online and offline) grassroots organizing, I set out to answer this question: do people expose themselves to political content on social media?

I decided to analyze users' friends (people they follow) on Twitter. Initially I scored users' "politicalness" by comparing their hashtags against a set of political hashtags collected using the Twitter API. When simply counting political hashtags proved too unreliable, I started exploring machine learning as a way to classify tweets.

Talking through the principles of machine learning with mentors was invaluable; their explanations helped me to understand the power of (and problems with) classification. Armed with a conceptual understanding, I explored both NLTK and sci-kit learn -- Python libraries useful for my kind of problem.

Several iterations of scoring algorithms later - hashtag counting, using NLTK's Naive Bayes to classify hashtags, and finally using scikit-learn's Bernoulli Naive Bayes to classify full-text tweets - my prototype calculates the average probability that each user's recent tweets belong to the "political" class. My training data consists of 60,000 tweets harvested in late November 2014 by querying for specific political and nonpolitical hashtags.

In the D3 visualization, bubbles represent any given user's most-followed friends. Bubble diameter is related to the number of followers that person has. Bubble color darkens in correlation with the average probability of political content, which can be approximately interpreted as a "percentage of political tweets."


##Current project state##

![ScreenShot](/static/images/scrn_cap0.png "Loading Data")

Search for any Twitter user by entering a Twitter handle into the search field.

The resulting visualiation depends on the "politicalness" score -- the output of the Naive Bayes classifier -- for each of the top 50 most influential friends. The score is a fraction between 0 and 1, determined by averaging probabilities given by a Naive Bayes classifier that any given tweet is political. 20 tweets are collected per friend, so the score may be only a measure of recent political dialogue.

The data is rendered in D3 as a bubble chart, with each bubble representing a Twitter account. Bubbles' opacity varies with the person's score -- dark bubbles mean more political, light bubbles less so. Bubble radii reflect the user's number of followers.

Bubbles can be hovered over for more information, or clicked on to reveal the user's 3 most recent tweets.

![ScreenShot](/static/images/scrn_cap3.png "On click")

## More about classification ##

Naive Bayes classifiers are often used often to classify text documents -- for example, classifying emails as spam or not-spam. Rather than using the classifier's predicted _label_ for tweets, however, I make use of the _probability_ that any given document (e.g. tweet) belongs to a specific class (e.g. political / not political). That value becomes the political score of a user.

Before firmly deciding on Naive Bayes, I compared its performance to a scikit-learn Logistic Regression algorithm.

    Metric| Bernoulli Naive Bayes  | Logistic Regression
    ------|------------- | -------------
 Precision| 87%          |  76%
    Recall| 88%          |  94%

The Naive Bayes algorithm correctly selected political tweets (true positives) 87% of the time, and identified 88% of all political labels (missing 12% of them) in the test set. Perhaps because of the ratio and size of my training data, Logistic Regression correctly labelled only 76% of tweets, although it missed fewer political tweets overall.

The Naive Bayes classifier used for generating "politicalness" scores tends to overpredict political content, probably because the training data is not large and diverse enough and does not reflect the true proportion of political content on Twitter.


##Moving forward:##

 - Show which features were most important in causing a user's timeline to receive a certain probability.

 - Increase the precision of my classifier, both by tuning it, by improving training data, and by testing other classifiers (i.e., Multinomial Bayes, K-near neighbors, SVM) for better performance.

 - Enable login with OAuth (currently using app auth) to deal with Twitter rate limiting in production

 - Reduce the number of API calls by storing data in memcache.

 - Continuously update the visualization, rather than wait for all tweets to be processed (using the Python 'time' library and New Relic's free APM tools, I can see that the bottleneck is the Twitter API; getting 20 tweets for 50 friends can take up to 40 seconds altogether!)

 - Write tests using Python's unittest or nosetest

 - Handle errors gracefully, beyond a simple flash message -- in particular errors caused by hitting the Twitter API rate limit

 ##Fun related projects##

  - Visualize liberal-conservative political leanings on Twitter, to investigate on a case-by-case basis when users have put themselves in a political echo chamber ("homophily") versus in conversation with politically diverse users.

 - Recommend diverse Twitter accounts that are either highly similar or highly different, politically, from the current user.


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

Now visit localhost:5000 in your browser!
