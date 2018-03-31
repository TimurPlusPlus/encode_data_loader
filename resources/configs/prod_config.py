data_dir        = "/data/encode/data_dir/"                                      # Root TF dir                           # A root data dir
metadata_file   = "/home/timurya/encode_data_loader/resources/input_data/metadata.tsv"    # Input encode table
script_dir      = "/home/timurya/encode_data_loader"                            # Current script dir
hg_dir          = "/home/timurya/hg19/hg19_chroms/"                             # Hg19 dir
chopped_hg_path = ""
stem_loops_dir  = "/home/timurya/stem_loops"
data_sample_dir = stem_loops_dir    # OR data_dir                               # Processed data dir
fetch_chrom_path= "/home/timurya/encode_data_loader/scripts/sh/fetchChromSizes.sh"

labels_dir      = [stem_loops_dir]

log_file        = "/data/encode/data_dir/log.log"


# OPTIONAL
space_to_save   = 20 * 1024 * 1024 * 1024                                        #1GB
chop_size       = 1048576

bedfile_extension='.bed'
zipfile_extension='.gz'
dirname_splitter='__'                                                           # To replace space character





