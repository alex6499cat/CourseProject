# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:07:59 2020

@author: Walter
"""


"""
Import relevant libraries
Pandas for data wrangling and datetime for performance checking
"""
import pandas as pd
import datetime as dt

"""
Import CSV file with one tweet per record
parse the date fields as such
"""

full_df = pd.read_csv("twcs.csv", na_filter= False, nrows=1000000,
                      parse_dates = ['created_at'], dtype = {'tweet_id': str,'in_response_to_tweet_id': str, 'inbound':bool, 'response_tweet_id':str })
full_df.head(300)

"""
Create a thread that encompasses all related tweets
The final tweet of each thread is the one with no next-tweet in the response_tweet_id
"""

mask = full_df["response_tweet_id"] == ""
thread = full_df[mask].copy()
thread.drop(["text","inbound","created_at","response_tweet_id","in_response_to_tweet_id"], axis = 1, inplace = True)
thread.head(3)

"""
Create the summary fields that will gather the data, for instance tweet_l will be a list of tweet_ids
separated by commas, and verify_time will have a True if the tweets in tweet_l have ascending timestamps
"""

thread["company_name"]=""
thread["tweet_l"] = ""
thread["author_l"] =""
thread["inbound_l"] = ""
thread["time_l"] = ""
thread["length"] = 0
thread["verify_thread"] = False
thread["verify_time"] = False
thread["verify_alternance"] = False
thread["inbound_first"] = False
thread.head(3)

"""
Indexing the dataframes. I ran into problems when indexing first from the pd.read_csv function.
It automatically used integers despite the field being imported as dtype string
"""

full_df.set_index("tweet_id", inplace = True)
thread.set_index("tweet_id", inplace = True)
print("Length of thread dataframe = ", len(thread))

"""
Sequentially process each thread in the thread dataframe
The id of the thread is the last tweet in the thread so it works backwards collecting the related tweets
"""

for row in range(len(thread)):
    thread_end = thread.index[row]
    prev_tweet = thread_end
    
    if row % 10000 == 0:
        print("Processing thread number: ", row , "time: ", dt.datetime.now().time())
    
    tweet_list = []
    author_list = []
    inbound_list = []
    time_list = []

    """
    Follow the tweets that correspond to a thread in the tweets dataframe
    using the previous tweet value, as we are going backwards from the end to the beginning
    """

    consistent_thread = True
    while (prev_tweet != "")  & consistent_thread:
        if (prev_tweet in full_df.index): 
            tweet_list.append(prev_tweet)
            my_list = full_df.loc[prev_tweet,["author_id","created_at","inbound","in_response_to_tweet_id"]]
            author_list.append(my_list[0])
            time_list.append(str(my_list[1]))
            inbound_list.append(str(my_list[2]))
            prev_tweet = my_list[3]
        else:
            consistent_thread = False
            
    """
    If the thread is consistent, meaning that all the tweets in the chain do exist,
    it starts building the lists of tweets, authors, etc. to write them in the appropriate fields of the thread dataframe
    """

    if consistent_thread:
        tweet_l       = '|'.join(tweet_list[::-1])
        author_l      = '|'.join(author_list[::-1])
        inbound_l     = '|'.join(inbound_list[::-1])
        time_l        = '|'.join(time_list[::-1])
        length        = len(tweet_list) 
        verify_thread = True
        inbound_first = inbound_list[-1]  
        verify_time   = True
        verify_alternance = True
        
        if "False" in inbound_list:
            company_name = author_list[inbound_list.index("False")]
        else:
            company_name = ""        
        if len(tweet_list) > 1:
            for i in range(len(tweet_list)-1):
                verify_alternance = verify_alternance & (inbound_list[i] != inbound_list[i+1])
                verify_time = verify_time & (time_list[i]>= time_list[i+1])
                
        thread.loc[thread_end, ["company_name","tweet_l","author_l","inbound_l","time_l","length","verify_thread","inbound_first","verify_time",
                                "verify_alternance"]] = [company_name,tweet_l,author_l,inbound_l,time_l,length,verify_thread,inbound_first,
                                                        verify_time, verify_alternance]  
                            
thread.head(4)
thread.to_csv(r'threads.csv')  