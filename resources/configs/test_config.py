data_dir="/home/timur/Desktop/masters/loader_test/data"                                           # A root data dir
metadata_file="../input_data/metadata.tsv"    # Input table
script_dir="../"
hg_dir="/home/timur/Desktop/masters/loader_test/hg19/"
chopped_hg_path=""
stem_loops_dir="/home/timur/Desktop/masters/loader_test/stem_loops"
fetch_chrom_path="/home/timur/Desktop/masters/encode_data_loader/scripts/sh/fetchChromSizes.sh"

log_file="/home/timur/Desktop/masters/loader_test/log.log"

space_to_save=1 * 1024 * 1024 * 1024                                       #1GB
chop_size=1000000

bedfile_extension='.bed'
zipfile_extension='.gz'
dirname_splitter='__'                                                       # To replace space character





