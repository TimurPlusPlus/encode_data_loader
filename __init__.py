import pandas as pd
import os
import sys

metadata_file = 'input_data/metadata.tsv'
columns = ['File accession', 'Output type', 'Experiment accession', 'Biosample type', 'Derived from', 'Size', 'md5sum', 'File download URL', 'Assembly']
assembly = 'hg19'

#Create a root dir
#data_dir = sys.argv[0]
data_dir = './'
os.makedirs(os.path.dirname(data_dir), exist_ok=True)

#Filter the DataFrame
df = pd.read_csv(metadata_file, sep='\t', usecols=columns)
filterred_df = df[df['Assembly'] == assembly]
filterred_df = filterred_df.drop('Assembly', 1)
test_df = filterred_df.head(10)

#Make folders and download files
for index, row in filterred_df.iterrows():
    new_dir = os.path.join(data_dir, row[])
os.makedirs(os.path.dirname(new_dir), exist_ok=True)







