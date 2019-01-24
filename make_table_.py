import pandas as pd
import fnmatch
import os, re
import random
# Here go the file distinctions acording to source (e.g. movie reviews, NIPS
# abstracts, baselines, etc.)
sys_tag="system"
docs_per_annotator=25
# These patterns must be contained in the CSV filenames.
sources=["_movies", "_experiments", "_abstracts", "_baseline", "_human_tab"]
regexs={sources[0]: sources[0]+"_\d{1,8}_(\d{3}).txt",
        sources[1]: sources[1]+"_d\d{5}t\.(\w+)",
        sources[2]: sources[2]+"_\d{4}_(\d{3})",
        sources[3]: sources[3]+"_d\d{5}t\.(\w+)",
        sources[4]: sources[4]+"_D\d{5}.M.100.T.([A-H])"
            }
#directory="/home/iarroyof/summ_features/csv_test/"
out_file="all_summ_tables_samp_%d__.csv" % docs_per_annotator
directory="/home/iarroyof/Documentos/summ_feats/RESULTS/"
files=[]
files_per=[]

# Open files for general features by summary.
for file in os.listdir(directory):
    if fnmatch.fnmatch(file, "*.csv"):
        if not "all" in file:
            if not "_per_" in file:
                files.append(file)
            else:
                files_per.append(file)

assert len(files_per) == len(files) # Features per sentence and features per sumary do not match.
tables=[]
tables_per=[]

# Get tables for column matching.
fils=[]
for file in files:
    tables.append(pd.read_csv(directory + file, sep='\t'))
    fils.append(file)

fils_per=[]
for file in files_per:
    tables_per.append(pd.read_csv(directory + file, sep='\t'))
    fils_per.append(file)
tables_headers=[]
for table in tables:
    tables_headers.append(list(table))
# Get unique headers in all tables for column consistency.
unique_headers=map( lambda x: x,
                    set(tables_headers[0]
                        ).intersection(*tables_headers) )

table_glo=pd.DataFrame(columns=unique_headers)
t = 0
#sources=["_movies", "_experiments", "_abstracts", "_baseline", "_human_tab"]
for table, fil in zip(tables,fils):
    for s_ in sources:
        if s_ in fil:
            table[sys_tag]=s_ + "_" + table[sys_tag]
    tables[t]=table
    t += 1

table_glo=pd.concat([table[unique_headers]
                        for table in tables],
                            axis=0).sort(columns=sys_tag).reset_index()
tables_headers=[]
for table in tables_per:
    tables_headers.append(list(table))

unique_headers=map( lambda x: x,
                    set(tables_headers[0]
                        ).intersection(*tables_headers) )

unique_headers=[header for header in unique_headers if (
                    header.endswith("_AVG") or \
                    header.endswith("_MAX") or \
                    header.endswith("_MIN") or \
                    header.endswith("_MED") or \
                    header == sys_tag
                )]

table_per=pd.DataFrame(columns=unique_headers)
t = 0
#sources=["_movies", "_experiments", "_abstracts", "_baseline", "_human_tab"]
for table, fil in zip(tables_per,fils_per):
    for s_ in sources:
        if s_ in fil:
            table[sys_tag]=s_ + "_" + table[sys_tag]
    tables_per[t]=table
    t += 1

table_per=pd.concat([table[unique_headers]
                        for table in tables_per],
                            axis=0).sort(columns=sys_tag).reset_index()

srcs_glo=[]
srcs_per=[]
for source in sources:
    src_glo=pd.DataFrame()
    idx=table_glo[sys_tag].str.contains(source, regex=True, na=False)

    src_glo=table_glo[idx].sort(columns=sys_tag)

    src_per=pd.DataFrame()
    idx=table_per[sys_tag].str.contains(source, regex=True, na=False).sort_index()
    src_per=table_per[idx].sort(columns=sys_tag)
    # Validate whether the annotator made equal or more than 'docs_per_annotator' summaries.

    unique_srcs=[s_ for s_ in src_glo[sys_tag].str.extract(regexs[source]).unique()
                    if not pd.isnull(s_) and src_glo[src_glo[sys_tag].str.contains(
                        s_+"(.txt|$)")
                    ].system.shape[0] >= docs_per_annotator
                ]
    if unique_srcs==[]:
        regexs.pop(source, None)
        continue
    for s_ in unique_srcs:
        win=src_glo[sys_tag].str.contains(s_+"(.txt|$)")
        rnd_indx=random.sample(src_glo[win].index, docs_per_annotator)

        srcs_glo.append(src_glo[win].ix[rnd_indx])
        srcs_per.append(src_per[win].ix[rnd_indx])

srcs_glo=pd.concat(srcs_glo, axis=0)
srcs_per=pd.concat(srcs_per, axis=0)

with open(directory+out_file, 'w') as f:
    pd.concat([srcs_glo,
               srcs_per],
              axis=1).T.drop_duplicates().T.to_csv(f, header=True)
