import ctypes
import datetime
import gzip
import hashlib
import logging
import os
import platform
import shutil
import sys
import urllib
from multiprocessing.dummy import Pool
import resources.test_config as conf
import pandas as pd
from scripts.logging.StreamToLogger import StreamToLogger


def download(url, file_name):
    logging.info('Downloading an archive to %s', file_name)
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    logging.info('The archive %s downloaded', file_name)


def get_md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_file_changed(file_name, md5):
    return get_md5(file_name) != md5


def get_device_available_space(dir_location):
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dir_location), None, None, ctypes.pointer(free_bytes))
        #return free_bytes.value / 1024 / 1024
        return 100000000000000000000000000000000000000
    disk = os.statvfs(dir_location)
    return float(disk.f_bsize*disk.f_bfree)


def gunzip(file_path, output_path):
    logging.info('Unzipping a file to %s', output_path)
    with gzip.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    logging.info('The file %s unzipped', output_path)

space_to_save = conf.space_to_save
data_dir = conf.data_dir
words_splitter = conf.dirname_splitter
file_extension = conf.bedfile_extension
zipfile_extension = conf.zipfile_extension
first_hierarchy_dir = 'Biosample type'
second_hierarchy_dir = 'Output type'
third_hierarchy_dir = 'Experiment accession'


def build_tree(row):
    # Check a free space on a drive
    if get_device_available_space(data_dir) < space_to_save:
        logging.error('The device available space is over')
        logging.info('The script work finished at %s', datetime.datetime.now())
        sys.exit(1)
    file_location = os.path.join(data_dir,
                                 row[first_hierarchy_dir].replace(' ', words_splitter),
                                 row[second_hierarchy_dir].replace(' ', words_splitter),
                                 row[third_hierarchy_dir].replace(' ', words_splitter),
                                 row['File accession'].replace(' ', words_splitter) + file_extension)
    # Check a file existing
    if not os.path.isfile(file_location):
        zipfile_location = file_location + zipfile_extension
        # Check the archive md5sum
        if not os.path.isfile(zipfile_location) or is_file_changed(zipfile_location, row['md5sum']):
            os.makedirs(os.path.dirname(zipfile_location), exist_ok=True)
            download(row['File download URL'], zipfile_location)
        gunzip(zipfile_location, file_location)
        os.remove(zipfile_location)


def configure_logger():
    logging.basicConfig(filename=conf.log_file, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl
    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

# A logger configuration
configure_logger()

start_time = datetime.datetime.now()
logging.info('The script started at %s', start_time)
metadata_file = conf.metadata_file
columns = ['File accession', 'Output type', 'Experiment accession', 'Biosample type', 'Derived from',
           'Size', 'md5sum', 'File download URL', 'Assembly']
assembly = 'hg19'


os.makedirs(data_dir, exist_ok=True)
logging.debug('Data dir: %s', data_dir)

# Filter the DataFrame
df = pd.read_csv(metadata_file, sep='\t', usecols=columns)
filtered_df = df[df['Assembly'] == assembly]
filtered_df = filtered_df.drop('Assembly', 1)

# For the testing purpose
test_df = filtered_df.head(5)
filtered_df = test_df
#
logging.debug('First 3 dataframe rows: %s', filtered_df.head(3))

# Collect all rows to send to multiprocessing
rows = []
for index, row in filtered_df.iterrows():
    rows.append(row)
pool = Pool(10)  # The pool of 10 processes
pool.map(build_tree, rows)
pool.close()
pool.join()

finish_time = datetime.datetime.now()
logging.info('The script work took %.2f seconds', (finish_time - start_time).total_seconds())





