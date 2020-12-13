"""
The objective is to calculate the difference in sentiment between the First Customer Tweet and the Last Customer Tweet of each conversation thread.
So that the difference (improvement) in sentiment is summarized by company and by time (year-month).
"""


import pandas as pd

senti_improve = pd.read_csv('thread_first_last_sentiment.csv', dtype = {'tweet_id': str})
senti_improve.head(50)

senti_improve.set_index('tweet_id', inplace = True)
senti_improve["first_senti_avg"] = 0
senti_improve["last_senti_avg"] = 0
senti_improve["senti_improve"] = 0
senti_improve["year_month"] = ""

senti_value_order = ["Very negative", "Negative", "Neutral", "Positive", "Very positive"]

def average_senti(senti_list_text):
    if type(senti_list_text) == str:
        senti_list = senti_list_text.split("|")
        senti_totalizer = 0
        for sentiment in senti_list:
            senti_totalizer += senti_value_order.index(sentiment)
        return senti_totalizer / len(senti_list)
    else:
        return 2
    
first_avg_col, last_avg_col, improve_col, year_month_col = senti_improve.columns.get_indexer(["first_senti_avg","last_senti_avg","senti_improve","year_month"])
first_sentiment_col, last_sentiment_col, timestamp_col = senti_improve.columns.get_indexer(["first_sentim_l","last_sentim_l","time_l"])

for row in range(len(senti_improve)):
    first_sentiment, last_sentiment, timestamp_list = senti_improve.iloc[row,[first_sentiment_col,last_sentiment_col, timestamp_col]]
    first_average = average_senti(first_sentiment)
    last_average = average_senti(last_sentiment)
    improvement = last_average - first_average
    year_month = timestamp_list[0:7]
    senti_improve.iloc[row,[first_avg_col,last_avg_col,improve_col,year_month_col ]]= [first_average,last_average, improvement, year_month]   
    
companies = senti_improve.groupby("company_name")
output = companies.agg({"length":"mean", "first_senti_avg":"mean", "last_senti_avg":"mean", "senti_improve":"mean", "verify_thread":"size"})

senti_improve.head()

senti_improve.to_csv(r'senti_improve_company_yearmonth.csv')  

output.to_csv(r'summary.csv')

companies_months = senti_improve.groupby(["company_name","year_month"])
output = companies_months.agg({"length":"mean", "first_senti_avg":"mean", "last_senti_avg":"mean", "senti_improve":"mean", "verify_thread":"size"})

output.to_csv(r'summary month.csv')