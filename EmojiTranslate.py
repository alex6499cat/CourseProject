import csv
import emoji
from joblib import Parallel, delayed
import multiprocessing


def removeEmoji(line):
    item = line
    for key in emoji.UNICODE_EMOJI:
        item = item.replace(key,emoji.UNICODE_EMOJI[key].replace(':'," "))
    return item

text = open("twcs.csv", "r")

x = open("output.csv","w")
num_cores = multiprocessing.cpu_count()

results = Parallel(n_jobs=num_cores)(delayed(removeEmoji)(i) for i in text)


x.writelines(results)

x.close()




