
import numpy as np
import scipy.stats as ss
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import logging
import itertools
import operator
from decimal import Decimal
from pdb import set_trace as st

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def feature_spectrum(human_ref, machines):
    return {f: 20.0 * np.log10((1 + machines[f]) / (1 + human_ref[f]))
                                                         for f in machines}

def create_table(pairs, file=None):

    header = sorted(list(set([c for _, c in pairs.keys()])))
    system = sorted(list(set([c for c, _ in pairs.keys()])))

    table = {"Annotator/summarizer": system}
    for h in header:
        col = []
        for s in system:
            try:
                col.append(pairs[(h, s)])
            except KeyError:
                continue
        table[h] = col
        table[h] = table[h] + ['--'] * (len(system) - len(table[h]))
    pd.DataFrame(table).to_csv(file, index=False)

# __main__()
parser = argparse.ArgumentParser()
parser.add_argument("--aspect", help="""Aspect ratio. aspect>1 reduces horizontal scale
                                        and aspect<1 reduces vectical scale.""",
                                        default=1.0, type=float)
parser.add_argument("--ndocs", help="""Documents per annotator to sample.""", default=25,
                                        type=int)
parser.add_argument("--feat", help="""If a specific feature is needed to be ploted.""",
                                        default=None)
parser.add_argument("--sp_bx", help="""If you need feature spectrum pass 'sp', and if
                                    you need boxplots pass 'bx'.""",
                                        default='bx')
parser.add_argument("--rot", help="""If you need to prepare the csv table for 1-page latex. 
                                     this rotates the headers and the cells.""",
                             default=False, action='store_true')
parser.add_argument("--cols", help="Toggle to output columnized version of p-values "
                                    "for headmapping.", default=False, action='store_true')
#parser.add_argument("--outdir", help="Output directory.", default=None)
args = parser.parse_args()

linewidth=2
aspect=args.aspect
docs_per_annotator=args.ndocs
vertical=True
in_file="all_summ_tables_samp_%d_dev_.csv" % docs_per_annotator
directory=""  #"/home/iarroyof/Documentos/summ_feats/RESULTS/"

non_feats=['Unnamed: 0', 'index', 'system', 'system.1']

if args.feat.startswith("inf"):
    may_feats=['IN_AVG', 'IN_MED','IN_MIN','IN_NNP','JJ_AVG',
            'named_entities','NNP','NNP_AVG','NNP_IN','NNP_MAX',
            'NNP_MED','NNP_MIN','NNP_NN','NNP_NNP','NNP_POS',
            'NNPS','NNPS_AVG','NNP_VBZ','NNS_MED','NNS_PERIOD',
            'no_corefs','no_tokens','sent_sentim_3','tok_sentim_2',
            'TotalRST','VBD','VBD_AVG','VBD_MAX','VBD_MED',
            'VBD_NNP','CC','CD_MAX','CD_MED']
    only_feat=['DATE', 'IN', 'NNP_NNP', 'no_openie', 
            'tok_sentim_1', 'tok_sentim_2', 'tok_sentim_3',
            'sent_sentim_1', 'sent_sentim_2', 'sent_sentim_3'] + may_feats
elif not args.feat == "all":
    only_feat=[args.feat]

sys_tag="system"
sources=["_movies", "_experiments", "_abstracts", "_baseline", "_human_tab"]
regexs={#sources[0]: sources[0]+"_\d{1,8}_(\d{3}).txt",
        sources[0]: sources[0]+"_\d{1,8}_(1[0-1][0-5]|09[5-9]).txt", # matches number in [95,115]
        sources[1]: sources[1]+"_d\d{5}t\.(\w+)",
        #sources[2]: sources[2]+"_\d{4}_(\d{3})",
        sources[2]: sources[2]+"_\d{4}_(1[0-1][0-5]|09[5-9])", # matches number in [95,115]
        sources[3]: sources[3]+"_d\d{5}t\.(\w+)",
        sources[4]: sources[4]+"_D\d{5}.M.100.T.([A-H])"
        }
final_src={sources[0]: "Humans_movi_",
           sources[1]: "Machines_soa_",
           sources[2]: "Humans_abstr_",
           sources[3]: "Machines_base_",
           sources[4]: "Humans_duc_"
               }

table_all = pd.read_csv(directory + in_file, sep=',')
src_feat = {}
for s_ in regexs:
    annotators = [s for s in table_all[sys_tag].str.extract(regexs[s_])[0].unique()
                                                                if not pd.isnull(s)]
    for a in annotators:
        src_feat[final_src[s_] + a] = table_all[table_all[sys_tag].str.contains(
                                                s_ + ".*" + a + "(.txt|$)")]
annotators = src_feat.keys()

median_phis_h = {}
median_phis_m_soa = {}
median_phis_m_base = {}

for feature in only_feat:
    phi_h = [list(src_feat[a][feature]) for a in annotators
                                                if a.startswith('Humans')]
    median_phis_h[feature] = np.median(
                            list(itertools.chain.from_iterable(phi_h))
                            )  # General human reference
    phi_m_soa = [list(src_feat[a][feature]) for a in annotators
                                                if a.startswith('Machines_soa_')]
    median_phis_m_soa[feature] = np.median(
                            list(itertools.chain.from_iterable(phi_m_soa))
                            )  # General human reference

    phi_m_base = [list(src_feat[a][feature]) for a in annotators
                                                if a.startswith('Machines_base_')]
    median_phis_m_base[feature] = np.median(
                            list(itertools.chain.from_iterable(phi_m_base))
                            )  # General human reference
if args.sp_bx == 'sp':
    spectrum_base = feature_spectrum(median_phis_h, median_phis_m_base)
    spectrum_soa = feature_spectrum(median_phis_h, median_phis_m_soa)

    spectra_base = sorted(spectrum_base.items(), key=operator.itemgetter(1))
    spectra_soa = [(f, spectrum_soa[f]) for f, _ in spectra_base]

    x, y_base = zip(*spectra_base)
    _, y_soa = zip(*spectra_soa)

    plt.xlabel('Compared features', fontsize=14)#, color='blue')
    plt.ylabel('Spectrum magnitude', fontsize=14)
    plt.title("Feature spectrum for State-of-the-Art"
            " and Baseline machine-made summaries", fontsize=11)
    plt.grid(True)
    plt.annotate('State-of-the-Art summaries', xy=(18, 2), xytext=(20, -4.8),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

    plt.annotate('Baseline summaries', xy=(20, 6), xytext=(15, 9),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

    plt.text(23, -1.0, "Human summaries")

    plt.margins(0.08)
    plt.xticks(range(len(x)), x, rotation='vertical', fontsize=10)
    plt.tight_layout()
    plt.locator_params(axis='y', nbins=20, tight=True)
    plt.plot(range(len(x)), y_soa, range(len(x)), y_base, range(len(x)),
         [0.0]*len(x), 'r--', linewidth=2.0)
    plt.show()

else:
    # Include the median of the column when it has less than 'docs_per_annotator'
    # items. The Mann-Whitneyu test is performed between annotators/summarizers
    # in order to verify/refute if humans and machines are statistically 
    # independent. The H_0 is that they are not independent, so a 
    # p-value <= 0.005 means they are independent.
    for feat in table_all:
        annotators_feat={}
        if feat not in non_feats and feat in only_feat:
            for i, a in enumerate(annotators):
                annotators_feat[a] = list(src_feat[a][feat])
                m = np.median(annotators_feat[a])
                annotators_feat[a] = annotators_feat[a] + [m] * (docs_per_annotator
                                                         - len(annotators_feat[a]))
            anns_dict = annotators_feat
            annotators_feat = pd.DataFrame(annotators_feat)
            asss = sorted(set(anns_dict.keys()))
            table = {"Annotator/summarizer": asss}
            repeats = []
            for A in asss:
                table[A] = ['--'] * len(asss)

            for A in asss:
                for B in asss:
                    j = asss.index(B)
                    if A == B:
                        continue
                    if (A, B) in repeats or (B, A) in repeats:
                        continue
                    else:
                        mwt = '{0:.2E}'.format(
                                    Decimal(ss.mannwhitneyu(anns_dict[A],
                                                        anns_dict[B]).pvalue))
                        if args.rot:
                            table[A][j] = "\\rot{%s}" % mwt if not mwt.endswith('E+0') \
                                            else "\\rot{%s}" % mwt.split('E')[0]
                        else:
                            table[A][j] = mwt if not mwt.endswith('E+0') \
                                            else mwt.split('E')[0]
                        repeats.append((A, B))
            out_name = feat + "_MannWhitneyMtx{}.csv" \
                            .format("_dev" if "_dev" in in_file else "")
            pd.DataFrame(table).to_csv(out_name, index=False)
            print("Saved Menn-Whitney matrix into {}".format(out_name))

            if args.cols:

                df = pd.read_csv(out_name, delimiter=',')
                x = [c for c in df.columns]
                y = df['Annotator/summarizer'].tolist()
                outl = []
                for i, a in enumerate(y):
                    for j, b in enumerate(x[1:]):
                        outl.append((a, b, df.iat[y.index(b), x.index(a)]))

                dfo = pd.DataFrame(outl, columns=["system_a", "system_b", "p_value"])
                heat_name = "{}_pvalues_heatmap.csv".format(feat)
                dfo[dfo.p_value != '--'].to_csv(heat_name)
                print("Saved Menn-Whitney heatmap into {}".format(heat_name))

            if args.rot:
                csv = feat + "_MannWhitneyMtx{}.csv".format("_dev" if "_dev" in in_file else "", 'w')
                with open(csv) as f:
                    lines = f.readlines()
                f.close()

                lines[0] = ",".join(["\\rot{%s}" % n for n in lines[0].split(',')])
                with open(csv, 'w') as fo:
                    for l in lines:
                        fo.write(l)

            ax=annotators_feat.plot(kind="box", vert=vertical, figsize=(17,15))
            ax.set_title(loc='center', label="Feature "+feat+
                        ": boxplots human/machine summarizers")
            ax.set_aspect(aspect)
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
