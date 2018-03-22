import os
import fnmatch
import re

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

transcription_dir = "./data"
stem_dir = "./stems"

coverage_name_pattern = re.compile("coverage_table_chr.*_\.bed")

stems = ["JKD21_KUKU", "Z228X3"]
stem_locations = {"JKD21_KUKU": "./stems/JKD21_KUKU"}

for path, dirs, files in os.walk(transcription_dir):
    for file in files:
        if coverage_name_pattern.match(file):
            path_to_transcription = os.path.join(path, file)

            for stem_name, stem_location in stem_locations.items():
                path_to_stem = os.path.join(stem_location, file)

                transcription_df = pd.read_csv(path_to_transcription, sep='\t', names=["chr", "start", "trans"])
                stem_df = pd.read_csv(path_to_stem, sep='\t', names=["chr", "start", "stem"])

                correlation_df = pd.merge(transcription_df, stem_df, on="start")
                correlation_df = correlation_df[["trans", "stem"]]
                cor = correlation_df.corr(method='pearson')

                f, ax = plt.subplots(figsize=(11, 9))
                sns.heatmap(cor, vmax=.3, center=0, linewidths=.5, cbar_kws={"shrink": .5})
                plt.show()




'''



table_file = "fact_coverage_table_chr3_.bed"
stem_file = "coverage_table_chr3_.bed"

table_df = pd.read_csv(table_file, sep='\t', names=["chr", "start", "trans"])
stem_df = pd.read_csv(stem_file, sep='\t', names=["chr", "start", "stem"])

print(table_df.head())
print(stem_df.head())

correlation_df = pd.merge(table_df, stem_df, on="start")
correlation_df = correlation_df[["trans", "stem"]]
print(correlation_df.head())
cor = correlation_df.corr(method='pearson')
print(cor.head())

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))


# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(cor, vmax=.3, center=0, linewidths=.5, cbar_kws={"shrink": .5})
plt.show()
print()

'''