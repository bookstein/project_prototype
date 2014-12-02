import os
import json
import time
import cPickle as pickle

from flask import Flask, url_for, request, render_template, redirect, flash
import tweepy

from friends import User, check_rate_limit

app = Flask(__name__)
app.secret_key = 'politicaltwitter'


TIME_TO_WAIT = 3  # in seconds
NUM_RETRIES = 2

PATH_TO_VECTORIZER = "politwit/vectorizer.pkl"
PATH_TO_CLASSIFIER = "politwit/classifierNB.pkl"

TEST_SET = ["bookstein", "ladygaga", "maddow"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ajax/user", methods=["POST"])
def get_user():
    api = connect_to_API()

    screen_name = request.json["screen_name"]

    if screen_name in TEST_SET:
        return redirect(url_for("get_prefetched", screen_name=screen_name))

    try:
        # check to make sure this user exists before proceeding
        user = api.get_user(screen_name=screen_name, include_entities=False)
        if user.id_str:
            return redirect(url_for("display_friends",
                            screen_name=screen_name))
        else:
            flash("Error: Twitter couldn't find that username.")
            return redirect(url_for("index"))

    except tweepy.TweepError as e:
        error_message = handle_error(e)
        flash(error_message)
        return redirect(url_for("index"))


@app.route("/get/display/<screen_name>")
def display_friends(screen_name):
    api = connect_to_API()

    with open(PATH_TO_CLASSIFIER, "rb") as f:
        classifier = pickle.load(f)

    with open(PATH_TO_VECTORIZER, "rb") as f:
        vectorizer = pickle.load(f)

    user = User(api, central_user=screen_name, user_id=screen_name)
    timeline = user.get_timeline(user.USER_ID, user.MAX_NUM_TWEETS)

    # initialize friend_scores object, which will pass friends and scores to d3
    friend_scores = {"name": user.USER_ID, "children": []}

    try:
        friends_ids = user.get_friends_ids(screen_name)

        friendlist = [user]

        for page in user.paginate_friends(friends_ids, 100):
            friends = process_friend_batch(user, page, api)
            friendlist.extend(friends)

        if len(friendlist) > user.MAX_NUM_FRIENDS:
            friendlist = get_top_influencers(friendlist, user.MAX_NUM_FRIENDS)

        for friend in friendlist:
            timeline = friend.get_timeline(friend.USER_ID,
                                           friend.MAX_NUM_TWEETS)
            friend.SCORE = friend.score(timeline, vectorizer, classifier)

            friend_scores["children"].append({"name": friend.SCREEN_NAME,
                                             "size": friend.NUM_FOLLOWERS,
                                             "score": friend.SCORE})

        json_scores = json.dumps(friend_scores)
        return json_scores

    except tweepy.TweepError as e:
        error_message = handle_error(e)
        flash(error_message)
        return redirect(url_for("index"))


def process_friend_batch(user, page, api):
    """
    Create User object for each friend in batch of 100 (based on pagination)
    """
    batch = []
    friend_objs = user.lookup_friends(f_ids=page)
    for f in friend_objs:
        friend = User(api, central_user=user.CENTRAL_USER, user_id=f.id)
        friend.NUM_FOLLOWERS = f.followers_count
        friend.SCREEN_NAME = f.screen_name
        batch.append(friend)
    return batch


def get_top_influencers(friendlist, count):
    """
    Get top influencers from user friends, as measured by # of followers.

    After requesting paginated friends, check "followers_count" attribute of
    each friend.

    Note:
    -----
    Run this function only if user has more than {count} friends.
    Currently, Twitter limits user timeline requests to 300
    (application auth) or 180 requests (user auth).

    Parameters:
    ----------
    List of all friend objects.
    Number of top influencers to output.

    Output:
    -------
    List of {count} most influential friends

    """

    sorted_by_influence = sorted(friendlist,
                                 key=lambda x: x.NUM_FOLLOWERS,
                                 reverse=True)
    friendlist = sorted_by_influence[:count]

    return friendlist


@app.route("/demo/prefetched/<screen_name>")
def get_prefetched(screen_name):
    time.sleep(TIME_TO_WAIT)
    if screen_name == "bookstein":
        return json.dumps({'name': 'bookstein', 'children': [{'score': 0.6621288434149878, 'name': 'nytimes', 'size': 14160089}, {'score': 0.6024210739190844, 'name': 'DalaiLama', 'size': 9834809}, {'score': 0.7532961655655628, 'name': 'BBCWorld', 'size': 8049266}, {'score': 0.7170098613172879, 'name': 'nprnews', 'size': 3061375}, {'score': 0.7411111088037284, 'name': 'maddow', 'size': 3044201}, {'score': 0.668490765740428, 'name': 'TheDailyShow', 'size': 2944827}, {'score': 0.6106084371672981, 'name': 'wikileaks', 'size': 2423037}, {'score': 0.7844805290743996, 'name': 'NickKristof', 'size': 1525849}, {'score': 0.9214918901147827, 'name': 'YourAnonNews', 'size': 1326447}, {'score': 0.3957033176556604, 'name': 'Medium', 'size': 1002287}, {'score': 0.8745964630221176, 'name': 'MotherJones', 'size': 455471}, {'score': 0.9478069469237381, 'name': 'HuffPostPol', 'size': 435314}, {'score': 0.4862231158061716, 'name': 'kanter', 'size': 404467}, {'score': 0.8444930591757265, 'name': 'democracynow', 'size': 347059}, {'score': 0.9260415189549398, 'name': 'ajam', 'size': 235139}, {'score': 0.9462528483917902, 'name': 'ACLU', 'size': 215827}, {'score': 0.9063116375558954, 'name': 'RBReich', 'size': 214252}, {'score': 0.8708490825538281, 'name': 'OccupyWallSt', 'size': 205603}, {'score': 0.43175795370399034, 'name': '99u', 'size': 189275}, {'score': 0.7244459940118697, 'name': 'pewresearch', 'size': 181212}, {'score': 0.6005260246749018, 'name': 'iraglass', 'size': 115326}, {'score': 0.8172435268595505, 'name': 'UpshotNYT', 'size': 99405}, {'score': 0.8154697883980356, 'name': 'AlterNet', 'size': 85902}, {'score': 0.2793861118514671, 'name': 'GA', 'size': 72873}, {'score': 0.6255953154263557, 'name': 'Revkin', 'size': 63501}, {'score': 0.3344072389905702, 'name': 'GirlsWhoCode', 'size': 61199}, {'score': 0.31305912636044037, 'name': 'TheMoth', 'size': 56476}, {'score': 0.9687524863997323, 'name': 'GlobalRevLive', 'size': 46335}, {'score': 0.5585787738587116, 'name': 'earthisland', 'size': 43248}, {'score': 0.5753698699586668, 'name': 'KQED', 'size': 42924}, {'score': 0.5769960776462038, 'name': 'tomtomorrow', 'size': 42916}, {'score': 0.8971033977000994, 'name': 'OccupyOakland', 'size': 41415}, {'score': 0.9102259061950695, 'name': 'SaveManning', 'size': 39019}, {'score': 0.27995737240395124, 'name': 'Daily_Good', 'size': 36056}, {'score': 0.3492342885188048, 'name': 'FoodCorps', 'size': 33250}, {'score': 0.8744117577919912, 'name': 'FactTank', 'size': 27073}, {'score': 0.3416501953318024, 'name': 'girldevelopit', 'size': 19914}, {'score': 0.7514660970444359, 'name': 'ProfessorCrunk', 'size': 18090}, {'score': 0.5843995473438215, 'name': 'quinnnorton', 'size': 17763}, {'score': 0.866547681131552, 'name': 'neworganizing', 'size': 17588}, {'score': 0.49393225605868346, 'name': 'MattBors', 'size': 16939}, {'score': 0.6116565283368856, 'name': 'aaronsw', 'size': 14906}, {'score': 0.7549212121248698, 'name': 'KuraFire', 'size': 13239}, {'score': 0.7790318818514511, 'name': 'susie_c', 'size': 12601}, {'score': 0.4780180119515844, 'name': 'realfoodnow', 'size': 12562}, {'score': 0.5764062616942909, 'name': 'hypatiadotca', 'size': 12090}, {'score': 0.6052069259993499, 'name': 'dnbornstein', 'size': 10058}, {'score': 0.24306846602456034, 'name': 'PopUpMag', 'size': 8707}, {'score': 0.6653150003042494, 'name': 'sarahjeong', 'size': 8388}, {'score': 0.2934325219344482, 'name': 'geekfeminism', 'size': 7826}]})

    elif screen_name == "ladygaga":
        return json.dumps({"name": "ladygaga", "children": [{"score": 0.3547027182525135, "name": "katyperry", "size": 60768976}, {"score": 0.7587056535986225, "name": "BarackObama", "size": 50506981}, {"score": 0.28375059983028433, "name": "YouTube", "size": 46801956}, {"score": 0.13000171349620165, "name": "britneyspears", "size": 39707252}, {"score": 0.25953023772882433, "name": "TheEllenShow", "size": 35326898}, {"score": 0.16016144301708746, "name": "selenagomez", "size": 24870949}, {"score": 0.17687825912418592, "name": "onedirection", "size": 21504665}, {"score": 0.1620363382779864, "name": "OfficialAdele", "size": 21302182}, {"score": 0.38486165255658933, "name": "Real_Liam_Payne", "size": 18599034}, {"score": 0.205003698177357, "name": "xtina", "size": 13509667}, {"score": 0.10233260985104779, "name": "ParisHilton", "size": 13005546}, {"score": 0.2806620153749058, "name": "RyanSeacrest", "size": 12962482}, {"score": 0.30244290267826834, "name": "iamwill", "size": 12597369}, {"score": 0.16885086259632545, "name": "tyrabanks", "size": 11833483}, {"score": 0.20090595060942612, "name": "MTV", "size": 11661204}, {"score": 0.8435341960114929, "name": "LeoDiCaprio", "size": 11514578}, {"score": 0.3273545438882518, "name": "TwitPic", "size": 8792867}, {"score": 0.16592759993012693, "name": "lindsaylohan", "size": 8636935}, {"score": 0.27994372328455325, "name": "eonline", "size": 7041818}, {"score": 0.7392520073776978, "name": "Starbucks", "size": 6935790}, {"score": 0.2827166905890308, "name": "iTunesMusic", "size": 6440633}, {"score": 0.512266769999232, "name": "106andpark", "size": 5708542}, {"score": 0.20930831604272587, "name": "Tip", "size": 5555052}, {"score": 0.3170270407371849, "name": "TheXFactor", "size": 5410779}, {"score": 0.2709828433977127, "name": "voguemagazine", "size": 4844006}, {"score": 0.25204867255098795, "name": "jimmykimmel", "size": 4564962}, {"score": 0.4368204075690628, "name": "AlanCarr", "size": 4309957}, {"score": 0.258507203681747, "name": "kendricklamar", "size": 4260002}, {"score": 0.4390874809013865, "name": "noaheverett", "size": 4230244}, {"score": 0.4048540247127489, "name": "LouisVuitton", "size": 3958621}, {"score": 0.4123733175100269, "name": "FactsOfSchool", "size": 3942280}, {"score": 0.269832246699181, "name": "KellyOsbourne", "size": 3873388}, {"score": 0.561028351925893, "name": "amandabynes", "size": 3717627}, {"score": 0.24161954483284917, "name": "KeshaRose", "size": 3648752}, {"score": 0.30669306896538917, "name": "tyleroakley", "size": 3395460}, {"score": 0.22569997997377592, "name": "Slash", "size": 3110809}, {"score": 0.2640821694043177, "name": "manuginobili", "size": 2724351}, {"score": 0.4052068225117976, "name": "lordemusic", "size": 2624554}, {"score": 0.15140544278989854, "name": "wwd", "size": 2592030}, {"score": 0.33436546762567804, "name": "greysonchance", "size": 2556696}, {"score": 0.2501239870137932, "name": "Metallica", "size": 2495683}, {"score": 0.3342955455093117, "name": "GMA", "size": 2487413}, {"score": 0.5697191609094797, "name": "cher", "size": 2375412}, {"score": 0.28413206537528995, "name": "NRJhitmusiconly", "size": 2368609}, {"score": 0.2529663994931427, "name": "adamlambert", "size": 2350151}, {"score": 0.027489780961743825, "name": "YSL", "size": 2343108}, {"score": 0.23201777459520595, "name": "billboard", "size": 2140189}, {"score": 0.16618408741016977, "name": "BBCR1", "size": 2024386}, {"score": 0.378451373866285, "name": "notch", "size": 1924544}, {"score": 0.12917281209457207, "name": "Versace", "size": 1852398}]})

    elif screen_name == "maddow":
        return json.dumps({"name": "maddow", "children": [{"score": 0.7587056535986225, "name": "BarackObama", "size": 50506923}, {"score": 0.34984109656174517, "name": "ladygaga", "size": 42937550}, {"score": 0.729327047713803, "name": "BillGates", "size": 18663406}, {"score": 0.3000318697852216, "name": "jimmyfallon", "size": 17805993}, {"score": 0.16482152289585864, "name": "KingJames", "size": 16609855}, {"score": 0.805547658340833, "name": "nytimes", "size": 14170779}, {"score": 0.23007870906993477, "name": "ActuallyNPH", "size": 11687151}, {"score": 0.3081891469423933, "name": "SHAQ", "size": 9070525}, {"score": 0.3728191205803314, "name": "NASA", "size": 8096044}, {"score": 0.731495062712785, "name": "BBCWorld", "size": 8057043}, {"score": 0.4410152225965082, "name": "stephenfry", "size": 8047759}, {"score": 0.3132623926663443, "name": "TheRock", "size": 7893701}, {"score": 0.4213552132216181, "name": "StephenAtHome", "size": 7181019}, {"score": 0.9944321603041233, "name": "BreakingNews", "size": 7093783}, {"score": 0.7152161211917873, "name": "TheEconomist", "size": 6614523}, {"score": 0.5734308529688705, "name": "johnlegend", "size": 6103057}, {"score": 0.45831022019314094, "name": "kobebryant", "size": 5887437}, {"score": 0.33852427333365315, "name": "SarahKSilverman", "size": 5754800}, {"score": 0.9098067421235037, "name": "Reuters", "size": 5542873}, {"score": 0.6540283809791257, "name": "WhiteHouse", "size": 5508234}, {"score": 0.38751852547907206, "name": "SteveMartinToGo", "size": 5427354}, {"score": 0.7773396135466004, "name": "andersoncooper", "size": 5394920}, {"score": 0.5736938837668353, "name": "HuffingtonPost", "size": 4906624}, {"score": 0.5315130974676451, "name": "Pontifex", "size": 4776374}, {"score": 0.31715758785608256, "name": "yokoono", "size": 4717456}, {"score": 0.7727783011180704, "name": "AP", "size": 4407133}, {"score": 0.5065754425154455, "name": "SamuelLJackson", "size": 4328006}, {"score": 0.4390874809013865, "name": "noaheverett", "size": 4230248}, {"score": 0.47320383861134996, "name": "KevinSpacey", "size": 3698268}, {"score": 0.35862110745691306, "name": "joelmchale", "size": 3526465}, {"score": 0.36856265567698926, "name": "JohnCleese", "size": 3512884}, {"score": 0.769053292010939, "name": "CBSNews", "size": 3430907}, {"score": 0.14478333073276, "name": "CFKArgentina", "size": 3352492}, {"score": 0.5860794618924325, "name": "UncleRUSH", "size": 3347563}, {"score": 0.7462693901411495, "name": "TheDailyShow", "size": 2946798}, {"score": 0.6356769181337458, "name": "Number10gov", "size": 2884467}, {"score": 0.6646146781046408, "name": "billmaher", "size": 2822882}, {"score": 0.7174577169437766, "name": "ElBaradei", "size": 2760411}, {"score": 0.47527517133949615, "name": "wilw", "size": 2739368}, {"score": 0.8528952622680317, "name": "jack", "size": 2736729}, {"score": 0.6593688921833918, "name": "neiltyson", "size": 2717653}, {"score": 0.3375304969063907, "name": "sethmeyers", "size": 2617194}, {"score": 0.5760166105891017, "name": "TODAYshow", "size": 2524121}, {"score": 0.7139224453263096, "name": "HillaryClinton", "size": 2481618}, {"score": 0.29621489299807385, "name": "MissyElliott", "size": 2461540}, {"score": 0.5157571647390748, "name": "MagicJohnson", "size": 2400704}, {"score": 0.7614863605912243, "name": "AJEnglish", "size": 2178563}, {"score": 0.33631664074903417, "name": "DAVID_LYNCH", "size": 2045830}, {"score": 0.7695654339618292, "name": "NBCNews", "size": 1932298}, {"score": 0.70230050976233, "name": "SenJohnMcCain", "size": 1924465}]})


def handle_error(e):
    if e.args[0][0]['code'] == "88":
        return "Rate limit exceeded: please wait a few minutes to retry."
    else:
        return "Error: We encountered an error while contacting Twitter: \n"
        + e.args[0][0]["message"]


def connect_to_API():
    """
    Create instance of tweepy API class with OAuth keys and tokens.
    """
    # initialize tweepy api object with auth, OAuth
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_SECRET_KEY = os.environ.get('TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_SECRET_TOKEN = os.environ.get('TWITTER_SECRET_TOKEN')

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY,
                               secure=True)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)
    api = tweepy.API(auth, cache=None, retry_count=NUM_RETRIES,
                     wait_on_rate_limit=False, wait_on_rate_limit_notify=False)

    return api

if __name__ == "__main__":
    app.run(debug=True)
