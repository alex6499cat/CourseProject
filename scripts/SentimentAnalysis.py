# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:24:39 2020

@author: Walter
"""
import stanza
import datetime as dt
import pandas as pd

corenlp_dir = './corenlp'

# Set the CORENLP_HOME environment variable to point to the installation location
import os
os.environ["CORENLP_HOME"] = corenlp_dir

# Import client module
from stanza.server import CoreNLPClient

threads = pd.read_csv('threads.csv', dtype = {'tweet_id': str} )
threads["first_sentim_l"] = ""
threads["last_sentim_l"] = ""
threads["first_tweet_text"] = ""
threads["last_tweet_text"] = ""

mask = (threads["length"] > 2) &  threads["verify_alternance"] & threads["inbound_first"] & threads["verify_thread"] & threads["verify_time"]  
thread_ok = threads[mask].copy()
thread_ok.set_index('tweet_id', inplace = True)

full_df = pd.read_csv("twcs-CleanedAndTranslatedEmoji.csv", na_filter= False, parse_dates = ['created_at'],
                      dtype = {'tweet_id': str,'in_response_to_tweet_id': str, 'inbound':bool, 'response_tweet_id':str })
full_df.set_index("tweet_id", inplace = True)

inbound_col, tweet_col, first_sentim_col, last_sentim_col, first_tweet_col, last_tweet_col = thread_ok.columns.get_indexer(["inbound_l","tweet_l","first_sentim_l", "last_sentim_l", "first_tweet_text","last_tweet_text"])
print("Starting a server with the Python \"with\" statement...")
with CoreNLPClient(annotators=['sentiment'], 
                   memory='6G', endpoint='http://localhost:9001', be_quiet=True) as client:
    print("Processing this number of valid threads: ", len(thread_ok))
    for row in range(119233,len(thread_ok)):           #hard coded the thread that has 140 middle_finger emoticons
        if row % 1000 == 0:
            print("Working on thread number: ", row, "time: ", dt.datetime.now().time())
        inbound_text, tweet_text = thread_ok.iloc[row,[inbound_col,tweet_col]]
        inbound_list = inbound_text.split("|")
        tweet_list = tweet_text.split("|")
        first_user_tweet = tweet_list[0]
        last_user_tweet = tweet_list[::-1][inbound_list[::-1].index("True")]
        first_tweet_text = full_df.loc[first_user_tweet,"text"]
        last_tweet_text = full_df.loc[last_user_tweet,"text"]
        first_doc = client.annotate(first_tweet_text)
        last_doc = client.annotate(last_tweet_text)
        first_sentiment = []
        last_sentiment = []
        for sentence in first_doc.sentence:
            first_sentiment.append(sentence.sentiment)
        for sentence in last_doc.sentence:
            last_sentiment.append(sentence.sentiment)
        thread_ok.iloc[row,[first_sentim_col,last_sentim_col, first_tweet_col, last_tweet_col]]= ['|'.join(first_sentiment),'|'.join(last_sentiment), first_tweet_text, last_tweet_text]
print("\nThe server should be stopped upon exit from the \"with\" statement.")

thread_ok.to_csv(r'thread_first_last_sentiment.csv')  