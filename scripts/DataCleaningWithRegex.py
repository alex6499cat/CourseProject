import csv
import re
from joblib import Parallel, delayed
import multiprocessing
import pandas as pd

regexes = ['@\d{3,9}','^(https?|ftp)://[^\s/$.?#].[^\s]*$','&amp;','^(https?|ftp)://[^\s/$.?#].[^\s]*$','\/[A-Z]{2,5}','\^[A-Z]{2,5}','https://t\..{2,100}','https://t\..{1,3}\/[1-9a-zA-Z]','\n']


translatedEmoji = pd.read_csv('twcs-translatedEmoji.csv')


print(translatedEmoji.head())
num_cores = multiprocessing.cpu_count()

for line, row in enumerate(translatedEmoji.itertuples(), 1):  # you don't need enumerate here, but doesn't hurt.
     for regex in regexes:
        translatedEmoji.at[row.Index, 'text'] = re.sub(regex, '', translatedEmoji.at[row.Index, 'text'])



translatedEmoji.to_csv('updatedAgain.csv')



