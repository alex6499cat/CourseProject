import csv
import re
from joblib import Parallel, delayed
import multiprocessing

regexes = ['@\d{3,9}','^(https?|ftp)://[^\s/$.?#].[^\s]*$','&amp;','\/[A-Z]{2}','\^[A-Z]{2}','https://t\..{2,100}\s','https://t\..{1,3}\/[1-9a-zA-Z]{1,100}\s']
regexReplaceWithQuote = ['https://t\..{2,100}\"','https://t\..{1,3}\/[1-9a-zA-Z]{1,100}\"']
regexReplaceWithComma = ['https://t\..{2,100}\,','https://t\..{1,3}\/[1-9a-zA-Z]{1,100}\,']

def removeEmoji(line):
    item = line
    for regex in regexes:
        item = re.sub(regex, '', item.rstrip())
    for regex in regexReplaceWithQuote:
        item = re.sub(regex, '"', item.rstrip())
    for regex in regexReplaceWithComma:
        item = re.sub(regex, ',', item.rstrip())
    item = item + '\n'
    return item

text = open("twcs.csv", "r")

numberOfLines = sum(1 for line in open("twcs.csv", "r"))
print(numberOfLines)



x = open("output-RemoveRegex.csv","w")
num_cores = multiprocessing.cpu_count()

results = Parallel(n_jobs=num_cores)(delayed(removeEmoji)(i) for i in text)

if(numberOfLines > 1000000):
    results = results[0:1000000]
x.writelines(results)

x.close()




