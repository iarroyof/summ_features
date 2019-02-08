# coding: utf-8
import csv

pvcsv = "C:\\Users\\DELL\\summ_features\\DATE_MannWhitneyMtx_dev.csv"

with open(pvcsv, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    print(reader.header)
    
import csv
import pandas as pd

pvcsv = "C:\\Users\\DELL\\summ_features\\DATE_MannWhitneyMtx_dev.csv"

df = pd.read_csv(pvcsv, delimiter=',')
df.columns
[c for c in df.columns[1:]]
df['Annotator/summarizer']
df['Annotator/summarizer'].tolist()
y = df['Annotator/summarizer'].tolist()
x = [c for c in df.columns[1:]]
df[x[0], y[0]]
df[x[0], y[1]]
df.at[x[0], y[1]]
df.at[0, 1]
df.iat[0, 1]
x[0]
df
df.iat[0, 0]
df.iat[1, 0]
df.iat[2, 0]
df.iat[0, 0]
x = [c for c in df.columns]
data = [(a, b, df.iat[x.index(), y.index()]) for a, b zip(x[1:], y)]
data = [(a, b, df.iat[x.index(), y.index()]) for a, b in zip(x[1:], y)]
data = [(a, b, df.iat[x.index(a), y.index(b)]) for a, b in zip(x[1:], y)]
len(x)
len(y)
x
outl = []
for a, b in zip(x[1:], y):
    outl.append(a, b, df.iat[x.index(a), y.index(b)])
    
for a, b in zip(x[1:], y):
    outl.append((a, b, df.iat[x.index(a), y.index(b)]))
    
    
a
b
x.index(a), y.index(b)
df.iat[0, 0]
df.iat[1, 0]
df.iat[0, 1]
for a, b in zip(x[1:], y):
    outl.append((a, b, df.iat[y.index(b), x.index(a)]))
    
outl
for a, b in zip(x[1:], y):
    outl.append((a, b, df.iat[y.index(b), x.index(a)]))
    
outl=[]
for i, a in enumerate(y):
    for j, b in enumerate(x[1:]):
        outl.append((a, b, df.iat[y.index(b), x.index(a)]))
        
outl
dfo = pd.DataFrame(outl, columns=["system_a", "system_b", "p-value"])
dfo
dfo.to_csv("NNP_NNP_pvalues_heatmap.csv")
get_ipython().run_line_magic('pwd', '')
dfo[df['p-values'] != '--'].to_csv("NNP_NNP_pvalues_heatmap.csv")
dfo.columns
dfo[df['p-value'] != '--'].to_csv("NNP_NNP_pvalues_heatmap.csv")
outl = []
for i, a in enumerate(y):
    for j, b in enumerate(x[1:]):
        outl.append((a, b, df.iat[y.index(b), x.index(a)]))
        
dfo = pd.DataFrame(outl, columns=["system_a", "system_b", "p_value"])
dfo[df.p_value != '--']
dfo[dfo.p_value != '--']
dfo[dfo.p_value != '--'].to_csv("NNP_NNP_pvalues_heatmap.csv")
get_ipython().run_line_magic('pwd', '')
get_ipython().run_line_magic('save', 'gen_columnar_pvalues ~0/')
