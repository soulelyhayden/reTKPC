import numpy as np

tweets = []
tDict = {}

phrase = ""

started = False


# find the first word for the markov chain
def findFirst():
    global firstWord, newTxt

    string = np.random.choice(tweets)

    # make sure it's not an empty string
    while string == "":
        string = np.random.choice(tweets)

    firstWord = np.random.choice(string.split())

    # make sure it's capitalized, and make sure you're still not searching an empty string
    while firstWord.islower():
        string = np.random.choice(tweets)

        while string == "":
            string = np.random.choice(tweets)

        firstWord = np.random.choice(string.split())

    newTxt = [firstWord]


# this is where the actual markov chain generation happens
def generateChain():
    global phrase

    findFirst()
    chainLength = np.random.randint(5, 25)
    phrase = ""
    for i in range(chainLength):
        try:
            newTxt.append(np.random.choice(tDict[newTxt[-1]]))
        except KeyError:
            "tried"
            continue

        phrase += " " + newTxt[i]

    # just making sure punctuation at the end of the sentence is correct, probably a better way to do this but this works for now
    if phrase.endswith(" "):
        phrase = phrase[:-1]
    if phrase.endswith(",") or phrase.endswith(":") or phrase.endswith(";"):
        phrase = phrase[:-1]
    if phrase.endswith(".") or phrase.endswith("?") or phrase.endswith("!"):
        return phrase[1:]
    else:
        return phrase[1:] + "."
