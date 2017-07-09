
import numpy as np
import scipy.stats as ss
import pandas as pd
import matplotlib.pyplot as plt
import re
#from pdb import set_trace as st

#data_m=np.array([1,2,3,4])   #(Means of your data)
#data_df=np.array([5,6,7,8])   #(Degree-of-freedoms of your data)
#data_sd=np.array([11,12,12,14])   #(Standard Deviations of your data)
linewidth=2
aspect=6
docs_per_annotator=25
vertical=True
in_file="all_summ_tables_samp_%d.csv" % docs_per_annotator
directory="/home/iarroyof/Documentos/summ_feats/RESULTS/"

non_feats=['Unnamed: 0', 'index', 'system', 'system.1']
only_feat=['DATE', 'IN', 'NNP_NNP', 'tok_sentim_2']
may_feats=['IN_AVG', 'IN_MED','IN_MIN','IN_NNP','JJ_AVG',
            'named_entities','NNP','NNP_AVG','NNP_IN','NNP_MAX',
            'NNP_MED','NNP_MIN','NNP_NN','NNP_NNP','NNP_POS',
            'NNPS','NNPS_AVG','NNP_VBZ','NNS_MED','NNS_PERIOD',
            'no_corefs','no_tokens','sent_sentiment_3','tok_sentim_2',
            'TotalRST','VBD','VBD_AVG','VBD_MAX','VBD_MED',
            'VBD_NNP','CC','CD_MAX','CD_MED']

sys_tag="system"
sources=["_movies", "_experiments", "_abstracts", "_baseline", "_human_tab"]
regexs={#sources[0]: sources[0]+"_\d{1,8}_(\d{3}).txt",
        sources[0]: sources[0]+"_\d{1,8}_(10\d).txt",
        sources[1]: sources[1]+"_d\d{5}t\.(\w+)",
        #sources[2]: sources[2]+"_\d{4}_(\d{3})",
        sources[2]: sources[2]+"_\d{4}_(1[0-5]{2}|09[5-9])",
        sources[3]: sources[3]+"_d\d{5}t\.(\w+)",
        sources[4]: sources[4]+"_D\d{5}.M.100.T.([A-H])"
            }
final_src={sources[0]: "Humans_movi_",
           sources[1]: "Machines_soa_",
           sources[2]: "Humans_abstr_",
           sources[3]: "Machines_base_",
           sources[4]: "Humans_duc_"
               }

table_all=pd.read_csv(directory + in_file, sep=',')

#means={feat:table_all[feat].mean() for feat in table_all if feat not in non_feats}
#medians={feat:table_all[feat].median() for feat in table_all if feat not in non_feats}
#sds={feat:table_all[feat].std() for feat in table_all if feat not in non_feats}
means={feat:table_all[feat].mean() for feat in table_all if feat not in non_feats and feat in only_feat}
medians={feat:table_all[feat].median() for feat in table_all if feat not in non_feats and feat in only_feat}
sds={feat:table_all[feat].std() for feat in table_all if feat not in non_feats and feat in only_feat}

src_feat={}
for s_ in regexs:
    annotators=[s for s in table_all[sys_tag].str.extract(regexs[s_]).unique() if not pd.isnull(s)]
    for a in annotators:
        src_feat[final_src[s_]+a]=table_all[table_all[sys_tag].str.contains(s_+".*"+a+"(.txt|$)")]

annotators=src_feat.keys()

for feat in table_all:
    annotators_feat={}
    if feat not in non_feats and feat in only_feat:
        #data_m=np.zeros(len(annotators))
        #data_sd=np.zeros(len(annotators))
        for i,a in enumerate(annotators):
        #    data_m[i]=src_feat[a][feat].mean()
        #    data_sd[i]=src_feat[a][feat].std()

            annotators_feat[a]=list(src_feat[a][feat])
        annotators_feat=pd.DataFrame(annotators_feat)
        ax=annotators_feat.plot(kind="box", vert=vertical, figsize=(17,15))
        ax.set_title(loc='center', label="Feature "+feat+
                        ": Confidence intervals for all human/machine summarizers")
        #ax.set_aspect(0.33)
        ax.set_aspect(0.1)
        ax.grid(color='r', linestyle='dashed', axis='y')
        ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
        ax.set_xlabel("Frequency within 100-word summaries")
        for box in ax.lines: box.set_linewidth(linewidth)
        print "Saving image: %s ..." % (directory+"figures/Feature_"+feat+
                    "_all_box_machine-human_samp_"+str(docs_per_annotator)+".png")

        plt.savefig(directory+"figures/Feature_"+feat+
                        "_all_box_machine-human_samp_"+str(docs_per_annotator)+".png")
        #plt.savefig(feat+"_all_box_machine-human_annotators.png")
        plt.clf()
        plt.close("all")

        #plt.errorbar(range(len(annotators)), data_m, yerr=ss.t.ppf(0.95, data_sd)*data_sd)
        #plt.xlim((-1,len(annotators)+1))
