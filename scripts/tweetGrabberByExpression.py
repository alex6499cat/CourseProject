import pandas as pd
import re

cleanedCsv = pd.read_csv('twcs-noEmojiCleaned.csv')
firstTweetIds = open("firstTweetIdsNoBlanks.csv", "r")

tweetIds = []
for tweetId in firstTweetIds:
    tweetIds.append(int(tweetId.rstrip()))

outputDictionary = {}
patterns = {'@Uber_Support':'uberTweets.txt','@AmazonHelp':'amazonTweets.txt','@AppleSupport':'appleTweets.txt'}
for pattern in patterns.keys():
    outputDictionary = {}
    for line, row in enumerate(cleanedCsv.itertuples(), 1): 
        if(re.match(pattern,str(cleanedCsv.at[row.Index, 'text']))):
                outputDictionary[str(cleanedCsv.at[row.Index, 'tweet_id'])] = str(cleanedCsv.at[row.Index, 'tweet_id']) + '|' + re.sub(pattern, '', str(cleanedCsv.at[row.Index, 'text']))


    print(len(outputDictionary))

    finalTweets = open(patterns[pattern], "w")

    finalResults = []

    for firstTweetId in tweetIds:
        if(str(firstTweetId) in outputDictionary):
            finalResults.append(outputDictionary[str(firstTweetId)]+"\n")

    finalResults = list(dict.fromkeys(finalResults))

    finalTweets.writelines(finalResults)