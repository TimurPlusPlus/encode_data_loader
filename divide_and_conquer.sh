#!/bin/bash

log="/data/encode/data_dir/log.log"
now=$(date)
echo "The script started at $now" >> $log


files=$(find /data/encode/data_dir/  -name '*.bed' -and -not -name 'chr?_.bed')
for file in $files
do
	cd /home/timurya/encode_data_loader
	
	new_dir_path="${file%.bed}"
	echo "New dir path $new_dir_path" >> $log
	mkdir -p $new_dir_path

	sort -k1,1 -k2,2n $file -o $file
	echo "Sort a file $file" >> $log

	file_name="../${file##*/}"
	echo "File name $file_name" >> $log
	cd $new_dir_path	
	awk -F'\t' '{printf ("%s\t%s\t%s\n", $1, $2, $3)>$1"_.bed"}' $file_name
done


now=$(date)
echo "The script finished at $now" >> $log
