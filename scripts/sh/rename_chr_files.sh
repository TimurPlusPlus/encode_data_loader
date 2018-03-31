#!/bin/bash

log=$1
data_sample_dir=$2

now=$(date)
echo "The rename_chr script started at $now" >> $log

files=$(find $data_sample_dir -name '*.bed')
for file in $files
do
        echo "A chromosome file $file" >> $log

        file_path="${file%/*}"                                  #Get path to chromosome file
        file_name="${file##*/}"                                 #Get chromosome file name
        chr_name="$(echo $file_name | awk -F"." '{print $1}')"  #Get chromosome name

        cd $file_path
        mv $file_name $chr_name"_.bed"
done


now=$(date)
echo "The build_coverages  script finished at $now" >> $log
