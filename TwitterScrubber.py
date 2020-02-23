import tweepy
import json
import ChainMaker
import re

# twitter api credentials would go here
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

twNum = 0


# starting the streamer
def setup():
    myStream = tweepy.Stream(auth=api.auth, listener=StreamListener(), tweet_mode='extended')
    myStream.filter(track=['#reTKPC'])


class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        try:
            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the wanted data from the Tweet
            text = datajson["text"]

            # other potentially useful information to grab
            '''screen_name = datajson['user']['screen_name']
            tweet_id = datajson['id']
            created_at = parser.parse(datajson['created_at'])
            replying_to = datajson['in_reply_to_screen_name']'''

            newTweet(text)

        except Exception as e:
            print(e)


# process what happens to a tweet when it comes in
def newTweet(tweet):

    # things have to be doen to it- remove newlines and special characters. Limit the length to the api length limit
    tweet = tweet.replace("/n", " ")
    tweet = ireplace("#reTKPC ", "", tweet)
    tweet = tweet.encode('ascii', 'ignore').decode('ascii')
    if len(tweet) > 115:
        tweet = tweet[:115]
        tweet += "..."

    # start the animations
    if ChainMaker.started is False:
        ChainMaker.started = True

    # this does all the dictionary stuff, adding all the new tweets to the markov chain dictionaries and adding oringal tweets to a list
    ChainMaker.tweets.append(tweet)

    ChainMaker.tDict.clear()
    chain = " ".join(ChainMaker.tweets)

    pairs = pair(chain.split())
    for wrd1, wrd2 in pairs:
        if wrd1 in ChainMaker.tDict.keys():
            ChainMaker.tDict[wrd1].append(wrd2)
        else:
            ChainMaker.tDict[wrd1] = [wrd2]


# takes care of other markov chain stuff for the dictionaries, making the phrases
def pair(splitTxt):
    for i in range(len(splitTxt) - 1):
        yield (splitTxt[i], splitTxt[i + 1])


# case-independent removal of the hashtag
def ireplace(old, new, text):
    index_l = text.lower().index(old.lower())
    return text[:index_l] + new + text[index_l + len(old):]
