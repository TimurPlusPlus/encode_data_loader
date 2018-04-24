import os

import pandas as pd
import resources.configs.prod_config as cnfg

data_dir = cnfg.data_dir

summary_df = pd.DataFrame(columns=["sample", "chr", "stem_name", "corr"])
for path, dirs, files in os.walk(data_dir):
    for file in files:
        if file == "correlations.csv":
            path_to_cor = os.path.join(path, file)
            cor_tab = pd.read_csv(path_to_cor, sep='\t', names=['chr', 'corr', 'stem_name', 'sample'], skiprows=1)
            cor_tab[['corr']] = cor_tab[['corr']].convert_objects(convert_numeric=True)
            cor_tab = cor_tab[cor_tab['corr'] > 0.7]
            cor_tab['sample'] = path.split(os.path.sep)[-1]
            summary_df = summary_df.append(cor_tab)

summary_df.to_csv(os.path.join(data_dir, "all_correlations.csv"), sep='\t', index=False)
