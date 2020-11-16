from gensim import models,corpora
from nltk.tokenize import word_tokenize 
from collections import defaultdict
from nltk.tokenize.treebank import TreebankWordDetokenizer

inputFileName = 'startOfThreadTweets.txt'
outputFileName = 'topicOfTweets.txt'
numberOfTopics = 30

tweets = open(inputFileName,"r")
stopwords = open('stopwords.txt',"r")
topicOfTweets = open(outputFileName,'w')


tweetList = tweets.read().splitlines() 

#Remove Stopwords
stoplist = stopwords.read().splitlines() 
texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in tweetList
]

#Count frequency of each word
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

#Remove words that only appear once
texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

#build dictionary and corpus
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

#create tfidf model of corpus
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

#create latent semantic index of tfidf model of corpus
lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=numberOfTopics) 

#loop through texts and query most fitting topic for each
matchedTopics = []
for text in texts:
    detokenizedText = TreebankWordDetokenizer().detokenize(text)
    results = lsi_model[dictionary.doc2bow(text)]
    greatestMatchedTopicNumber = -1
    greatestTopicMatch = -1
    for result in results:
        if(result[1] > greatestTopicMatch):
            greatestMatchedTopicNumber = result[0]
            greatestTopicMatch = result[1]
    topicOfTweets.write(detokenizedText + '|' + str(greatestMatchedTopicNumber)+ '\n')
    


