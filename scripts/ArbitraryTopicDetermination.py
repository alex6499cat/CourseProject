from gensim import models,corpora,utils
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from nltk.tokenize import word_tokenize 
from collections import defaultdict
from nltk.tokenize.treebank import TreebankWordDetokenizer
import spacy

inputFileName = 'StartingThreadTweetsByCompany/uberTweets.txt'
outputFileName = 'topicResults/UberTopics.txt'
topicModelName = 'topicResults/UberTopicModel.txt'
numberOfTopics = 20

tweets = open(inputFileName,"r")
stopwords = open('stopwords.txt',"r")
topicOfTweets = open(outputFileName,'w')
topicModel = open(topicModelName,"w")

mainList = tweets.read().splitlines()
tweetList = []
idList = []
for listItem in mainList:
    tweetList.append(listItem.split('|')[1])
    idList.append(listItem.split('|')[0])

nlp = spacy.load('en', disable=['parser', 'ner'])

def sent_to_words(sentences):
    for sentence in sentences:
        yield(utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


#Remove Stopwords
stoplist = stopwords.read().splitlines() 
texts = [
    [word for word in document.lower().split() if word not in stoplist]
    for document in tweetList
]

tweetList = list(sent_to_words(texts))



# Build the bigram and trigram models
bigram = models.Phrases(tweetList, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = models.Phrases(bigram[tweetList], threshold=100)  

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = models.phrases.Phraser(bigram)
trigram_mod = models.phrases.Phraser(trigram)




texts = make_bigrams(texts)

nlp = spacy.load('en', disable=['parser', 'ner'])

# Do lemmatization keeping only noun, adj, vb, adv
texts = lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])


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

#create latent  Latent Dirichlet Allocation of tfidf model of corpus
lsi_model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=numberOfTopics,per_word_topics=True) 

topicModel.write(str(lsi_model.print_topics()))

#loop through texts and query most fitting topic for each
matchedTopics = []
count = 0
for text in texts:
    detokenizedText = TreebankWordDetokenizer().detokenize(text)
    results = lsi_model[dictionary.doc2bow(text)]
    greatestMatchedTopicNumber = -1
    greatestTopicMatch = float(-1)
    for result in results:
        for element in result:
            index,score = element
            dog = str(score)
            if (type(score) is not list) and float(dog) > greatestTopicMatch and text:
                greatestMatchedTopicNumber = index
                greatestTopicMatch = score
    if(greatestTopicMatch > -1):
        topicOfTweets.write(idList[count]+'|'+ detokenizedText + '|' + str(greatestMatchedTopicNumber)+ '\n')
    count += 1


    


