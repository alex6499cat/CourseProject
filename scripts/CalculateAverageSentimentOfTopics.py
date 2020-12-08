import pandas as pd


sentiments = pd.read_csv('senti_improve_company_yearmonth.csv')

deltaTopics = open('DeltaTopics.txt',"r")

deltaStart = open('deltaStartTweetAverageSentimentByTopic.txt',"w")
deltaEnd = open('deltaLastTweetAverageSentimentByTopic.txt',"w")
deltaImprove = open('deltaImproveTweetAverageSentimentByTopic.txt',"w")
deltaTopics = deltaTopics.read().splitlines()

firstSentimentTopicMap = {}
firstSentimentAverages = {}

lastSentimentTopicMap = {}
lastSentimentAverages = {}

improveSentimentTopicMap = {}
improveSentimentAverages = {}


for x in range(10):
    firstSentimentTopicMap[str(x)] = []
    lastSentimentTopicMap[str(x)] = []
    improveSentimentTopicMap[str(x)] = []

print(firstSentimentTopicMap)

for line, row in enumerate(sentiments.itertuples(), 1):  
    if(sentiments.at[row.Index, 'company_name'] == 'Delta'):
        firstTweetIdSentiment = sentiments.at[row.Index, 'tweet_l'].split('|')[0]
        firstSentimentAverage = sentiments.at[row.Index, 'first_senti_avg']
        lastSentimentAverage = sentiments.at[row.Index, 'last_senti_avg']
        improveSentimentAverage = sentiments.at[row.Index, 'senti_improve']

        for deltaTopic in deltaTopics:
            deltaTopic = deltaTopic.split('|')
            deltaTweetId = deltaTopic[0]
            topic = deltaTopic[2]
            if(firstTweetIdSentiment.strip() == deltaTweetId.strip()):

                firstSentimentTopicMap[topic.strip()].append(float(firstSentimentAverage))
                lastSentimentTopicMap[topic.strip()].append(float(lastSentimentAverage))
                improveSentimentTopicMap[topic.strip()].append(float(improveSentimentAverage))




for x in range(10):

    deltaStart.write(str(x) + '|' + str(sum(firstSentimentTopicMap[str(x)])/len(firstSentimentTopicMap[str(x)])) + '\n')
    deltaEnd.write(str(x) + '|' + str(sum(lastSentimentTopicMap[str(x)])/len(lastSentimentTopicMap[str(x)])) + '\n')

    deltaImprove.write(str(x) + '|' + str(sum(improveSentimentTopicMap[str(x)])/len(improveSentimentTopicMap[str(x)])) + '\n')

