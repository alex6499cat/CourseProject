# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:24:39 2020

@author: Walter
"""
# Import stanza
import stanza
import pandas as pd

corenlp_dir = './corenlp'

# Set the CORENLP_HOME environment variable to point to the installation location
import os
os.environ["CORENLP_HOME"] = corenlp_dir

# Import client module
from stanza.server import CoreNLPClient

threads = pd.read_csv('threads.csv')


print("Starting a server with the Python \"with\" statement...")
with CoreNLPClient(annotators=['sentiment'], 
                   memory='4G', endpoint='http://localhost:9001', be_quiet=True) as client:
    text = "Albert Einstein was a German-born theoretical physicist. He developed the theory of relativity. I am not very happy."
    document = client.annotate(text)

    for sent in document.sentence:
        print(sent.sentiment)

print("\nThe server should be stopped upon exit from the \"with\" statement.")