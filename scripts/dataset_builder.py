import os
import re
import pandas as pd
import resources.configs.prod_config as cnfg


hg_dir = cnfg.hg_dir
data_dir = cnfg.data_dir
labels_dir = cnfg.labels_dir
coverage_name_pattern = re.compile("coverage_table_(chr.*)_\.bed")
hg_filename_pattern = re.compile("chr.*_.bed")

# Fill the df by coverages from bed files
def collect(summary_df, data_dir):
    for path, dirs, files in os.walk(data_dir):
        sample_name = os.path.basename(os.path.normpath(path))
        sample_df = pd.DataFrame(columns=["chr", "start", sample_name])
        for file in files:
            if coverage_name_pattern.match(file):
                path_to_file = os.path.join(path, file)
                file_df = pd.read_csv(path_to_file, sep='\t',
                                      usecols=[0, 1, 3],
                                      names=["chr", "start", sample_name])
                sample_df = sample_df.append(file_df)
        if not sample_df.empty:
            summary_df = pd.merge(summary_df, sample_df, on=["chr", "start"], how='left')
    return summary_df


summary_df = pd.DataFrame(columns=["chr", "start"])
# Build preliminary dataset
for path, dirs, files in os.walk(hg_dir):
    for file in files:
        if hg_filename_pattern.match(file):
            path_to_hg = os.path.join(path, file)
            file_df = pd.read_csv(path_to_hg, sep='\t',
                                           usecols=[0, 1],        # Read chr name and start position
                                           names=["chr", "start"])
            summary_df = summary_df.append(file_df)

# Collect features
summary_df = collect(summary_df, data_dir)

# Collect labels
for label in labels_dir:
    summary_df = collect(summary_df, label)

summary_df.to_csv(os.path.join(data_dir, "tf_stem-loops.csv"), sep='\t', index=False)