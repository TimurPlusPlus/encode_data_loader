#!/bin/bash

log=$1
data_dir=$2
script_dir=$3

now=$(date)
echo "The sort_and_split script started at $now" >> "${log}"

files=$(find $data_dir  -name '*.bed' -and -not -name 'chr?_.bed')
for file in $files
do
	cd $script_dir                                                              #Move back to the script to not have problems with mkdir
	
	new_dir_path="${file%.bed}"                                                 #A file path without extension
	echo "New dir path $new_dir_path" >> "${log}"
	mkdir -p $new_dir_path

	sort -k1,1 -k2,2n $file -o $file
	echo "Sort a file $file" >> "${log}"

	file_name="../${file##*/}"
	echo "File name $file_name" >> "${log}"
	cd $new_dir_path	
	awk -F'\t' '{printf ("%s\t%s\t%s\n", $1, $2, $3)>$1"_.bed"}' $file_name     #Split a bed file by chromosomes
done


now=$(date)
echo "The sort_and_split script finished at $now" >> "${log}"
