#Politicization on Twitter#

A project for Hackbright Academy, Fall 2014.

Using data from Twitter's Search and REST API, as well as scikit-learn's Bernoulli Naive Bayes classifer, visualize the recent intensity of political activity within any Twitter user's friend group in an interactive bubble chart.

##About the project##

I chose my project inspired by my interest in social movements and informed by a past internship at Causes.com, a tech start-up that made tools for online activism. Towards the beginning of the project period, I learned that only 23% of millenials planned to vote in the 2014 midterm elections. I wondered how social media might have an impact on voter turnout: do people have political friends on social media? If so, do they put themselves in an echo chamber of like-minded people?

I began scoring Twitter users' tweets by counting political hashtags. Later, when simply counting hashtags proved too unreliable, I started exploring machine learning as a way to classify tweets.

Talking through the principles of machine learning with mentors was invaluable; their explanations helped me to understand the problems and powers of classification. Armed with a conceptual understanding, I explored both NLTK and sci-kit learn -- python machine learning modules useful for my kind of problem.

Several iterations of scoring algorithms later - simple hashtag counting, using NLTK's Naive Bayes to classify hashtags, and finally using scikit-learn's Bernoulli Naive Bayes to classify full-text tweets - my project identifies the average probability that a user's recent tweets are political. My training data consists of 60,000 tweets harvested in late November 2014 by querying for specific political and nonpolitical hashtags.


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

![ScreenShot](/static/images/scrn_cap0.png "Loading Data")

Search for any Twitter user by entering a Twitter handle into the search field.

The result is a "politicalness" score for each of the top 50 most influential friends (people that user follows). The score is a fraction between 0 and 1 -- determined by averaging probabilities given by a Naive Bayes classifier that any given tweet is political. 20 tweets are collected per friend, so the score may be only a measure of recent political dialogue.

The data is rendered in d3 as a bubble chart, with each bubble representing a Twitter account. Bubbles' opacity varies with the person's score -- dark bubbles mean more political, light bubbles less so. Bubble radii reflect the number of followers.

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

The Naive Bayes classifier used for generating "politicalness" scores tends to overpredict political content, probably because the training data is not diverse enough and does not reflect the true proportion of political content on Twitter.


##Moving forward:##

 - Visualize liberal-conservative political leanings on Twitter, to investigate on a case-by-case basis when users have put themselves in a political echo chamber ("homophily") versus in conversation with politically diverse users.

 - Recommend diverse Twitter accounts that are either highly similar or highly different, politically, from the current user.

 - Show which features were most important in causing a user's timeline to receive a certain political score.

 - Increase the precision of my classifier, both by tuning it, by improving training data, and by testing other classifiers (i.e., Multinomial Bayes, K-near neighbors, SVM) for better performance.

 - Enable login with OAuth (currently using app auth) to deal with Twitter rate limiting in production

 - Reduce the number of API calls by storing data in memcache.

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

Now visit localhost:5000 in your browser!
