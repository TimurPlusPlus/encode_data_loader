import pandas as pd
import os
import sys

metadata_file = './input_data/metadata.tsv'
columns = ['File accession', 'Output type', 'Experiment accession', 'Biosample type', 'Derived from',
           'Size', 'md5sum', 'File download URL', 'Assembly']
assembly = 'hg19'
first_hierarchy_dir = 'Biosample type'
second_hierarchy_dir = 'Output type'
third_hierarchy_dir = 'Experiment accession'

# Create a root dir
#data_dir = sys.argv[0]
data_dir = './data'
os.makedirs(os.path.dirname(data_dir), exist_ok=True)

# Filter the DataFrame
df = pd.read_csv(metadata_file, sep='\t', usecols=columns)
filtered_df = df[df['Assembly'] == assembly]
filtered_df = filtered_df.drop('Assembly', 1)

# For the testing purpose
test_df = filtered_df.head(10)
filtered_df = test_df
print(test_df.head())


# Make folders and download files

# Maybe it would be better to sort the data before iterating
for index, row in filtered_df.iterrows():
    # Check a free space on a drive
    new_dir = os.path.join(data_dir, row[first_hierarchy_dir])
    # Check a file existing and md5
    # Download a file


os.makedirs(os.path.dirname(new_dir), exist_ok=True)







