data_dir        = "/home/timur/Desktop/masters/loader_test/data"                # Root TF dir                           # A root data dir
metadata_file   = "../input_data/metadata.tsv"                                  # Input encode table
script_dir      = "../"                                                         # Current script dir
hg_dir          = "/home/timur/Desktop/masters/loader_test/hg19/"               # Hg19 dir
chopped_hg_path = ""
stem_loops_dir  = "/home/timur/Desktop/masters/loader_test/stem_loops"
data_sample_dir = stem_loops_dir    # OR data_dir                               # Processed data dir
fetch_chrom_path= "/home/timur/Desktop/masters/encode_data_loader/scripts/sh/fetchChromSizes.sh"

labels_dir      = [stem_loops_dir]

log_file        = "/home/timur/Desktop/masters/loader_test/log.log"


# OPTIONAL
space_to_save   = 1 * 1024 * 1024 * 1024                                        #1GB
chop_size       = 1000000

bedfile_extension='.bed'
zipfile_extension='.gz'
dirname_splitter='__'                                                           # To replace space character





