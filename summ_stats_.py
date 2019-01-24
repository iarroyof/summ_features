from __future__ import print_function
from statsmodels.compat import urlopen
import numpy as np
np.set_printoptions(precision=4, suppress=True)
import statsmodels.api as sm
import pandas as pd
pd.set_option("display.width", 100)
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.graphics.api import interaction_plot, abline_plot
from statsmodels.stats.anova import anova_lm

from pdb import set_trace as st

features = ["IN_AVG", "IN_MED","IN_MIN", "IN_NNP", "JJ_AVG", "named_entities",
            "NNP", "NNP_AVG", "NNP_IN", "NNP_MAX", "NNP_MED", "NNP_MIN",
            "NNP_NN",  ]

directory="/home/iarroyof/Documentos/summ_feats/RESULTS"

#try:
summ_table = pd.read_csv(directory+'/all_summ_tables_samp_25_.csv')
#except:  # recent pandas can read URL without urlopen
#    url = 'http://stats191.stanford.edu/data/salary.table'
#    fh = urlopen(url)
#    salary_table = pd.read_table(fh)
#    salary_table.to_csv('salary.table')
st()
#E = salary_table.E
#M = salary_table.M
#X = salary_table.X
#S = salary_table.S

