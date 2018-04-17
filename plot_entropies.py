from math import log
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import pandas as pd
import matplotlib.pyplot as plt

vectorizer = TfidfVectorizer(lowercase=True)

file_list = sys.argv[1] #"/home/iarroyof/data/sumrepo_duc2004/SOAsums/files_soa.ICSISumm"

with open(file_list) as f:
    files = [name.strip() for name in f.readlines()]

docs = []
for file in files:
    with open(file) as f:
        docs.append(" ".join(f.readlines()))

vectorizer.fit(docs)
vocab = vectorizer.vocabulary_

tokenize = vectorizer.build_tokenizer()

def logent(x):
    if x<=0:
        return 0
    else:
        return -x*log(x)

def entropy(lis):
    return sum([logent(elem) for elem in lis])

from pdb import set_trace as st

probs_bySumm = []
for summary in docs:
    words = tokenize(summary)
    probs_bySumm.append([words.count(word)*1.0/len(words) for word in vocab])

entropies = []
for probs in probs_bySumm:
    #print("%s\t%f" % (file_list.split(".")[-1], entropy(probs)))
    entropies.append(entropy(probs))

df = pd.DataFrame(entropies, columns=[file_list.split(".")[-1]])
df.boxplot(column=file_list.split(".")[-1], return_type='axes')
plt.show()
