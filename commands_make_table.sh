# Set the output file as all_summ_tables_samp_25_dev.csv in the make_table_py script
python make_trable.py
# Remove indexes and rearange 'system' column to the beginning.
fil=all_summ_tables_samp_25_dev.csv; paste -d"," <(awk -F"," '{ print $206}' $fil) <(cols="3-205"; cut -d"," -f"$cols" $fil) <(cols="207-"; cut -d"," -f"$cols" $fil) > all_summ_tables_samp_25_dev_.csv

python -c "fa = open('all_summ_tables_samp_25__.csv'); Fa = fa.readlines(); fb = open('all_summ_tables_samp_25_.csv'); ia=205; ib=0; l = [n for n, ls in enumerate(zip(Fa, fb)) if ls[0].split(',')[ia] == ls[1].split(',')[ib]]; 
for i in l[1:]:
    del Fa[i]
with open('all_summ_tables_samp_25_dev.csv', 'w') as f:
    for l in Fa:
        f.write('%s' % l)
"
