import gzip
import hashlib
import urllib
import shutil
import pandas as pd
import os
import logging
import datetime
import sys


def download(url, file_name):
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def get_md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_file_changed(file_name, md5):
    return get_md5(file_name) == md5


def get_uncompressed_size(file_name):
    with open(file_name, 'r') as fileobj:
        isize = gzip.read32(fileobj)  # may exceed 2GB
    return isize


def get_device_available_space(dir_location):
    disk = os.statvfs(dir_location)
    return float(disk.f_bsize * disk.f_bfree)


def gunzip(file_path, output_path):
    with gzip.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

# A logger configuration
logging.basicConfig(filename='./data_loader.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logging.info('The script started at %s', datetime.datetime.now())
metadata_file = './input_data/metadata.tsv'
columns = ['File accession', 'Output type', 'Experiment accession', 'Biosample type', 'Derived from',
           'Size', 'md5sum', 'File download URL', 'Assembly']
assembly = 'hg19'
first_hierarchy_dir = 'Biosample type'
second_hierarchy_dir = 'Output type'
third_hierarchy_dir = 'Experiment accession'


# Create a root dir
#data_dir = sys.argv[0]
#available_memory_volume = sys.argv[1]
#available_memory_volume = sys.argv[1]
space_to_save = 20 * 1024 * 1024 * 1024  # 20GB
data_dir = './data'
words_splitter = '__'
file_extension = '.bed'
zipfile_extension = '.gz'

os.makedirs(os.path.dirname(data_dir), exist_ok=True)
logging.debug('Data dir: %s', data_dir)

# Filter the DataFrame
df = pd.read_csv(metadata_file, sep='\t', usecols=columns)
filtered_df = df[df['Assembly'] == assembly]
filtered_df = filtered_df.drop('Assembly', 1)

# For the testing purpose
test_df = filtered_df.head(10)
filtered_df = test_df
#
logging.debug('First 3 dataframe rows: %s', filtered_df.head(3))

# Make folders and download files
for index, row in filtered_df.iterrows():
    # Check a free space on a drive
    if get_device_available_space(data_dir) < space_to_save:
        logging.error('The device available space is over')
        logging.info('The script work finished at %s', datetime.datetime.now())
        exit(1)

    file_location = os.path.join(data_dir,
                                 row[first_hierarchy_dir].replace(' ', words_splitter),
                                 row[second_hierarchy_dir].replace(' ', words_splitter),
                                 row[third_hierarchy_dir].replace(' ', words_splitter),
                                 row['File accession'].replace(' ', words_splitter) + file_extension)

    # Check a file existing and md5
    if not os.path.isfile(file_location):  # or is_file_changed(file_location, row['md5sum']):
        zipfile_location = file_location + zipfile_extension
        logging.info('Downloading an archive to %s', zipfile_location)
        os.makedirs(os.path.dirname(zipfile_location), exist_ok=True)
        download(row['File download URL'], zipfile_location)
        logging.info('The file downloaded')
        logging.info('Unzipping a file to %s', file_location)
        # Unzip the file
        gunzip(zipfile_location, file_location)
        logging.info('The file unzipped')
        # Delete the archive
        os.remove(zipfile_location)

logging.info('The script work finished at %s', datetime.datetime.now())





