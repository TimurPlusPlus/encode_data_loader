#!/bin/bash

log=$1
hg_dir=$2
data_sample_dir=$3

now=$(date)
echo "The build_coverages for stem-loops script started at $now" >> $log

files=$(find $data_sample_dir -name 'chr*_.bed')
for file in $files
do
        echo "A chromosome file $file" >> $log

        file_path="${file%/*}"                  #Get path to chromosome file
        file_name="${file##*/}"                 #Get chromosome file name
        hg_file=$hg_dir$file_name
        echo "A hg19 file $hg_file" >> $log

        coverage_file=$file_path"/coverage_table_"$file_name
        bedtools coverage -a $hg_file -b $file | awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$7}'  > $coverage_file
        echo "A coverage file $coverage_file" >> $log

        sort -k1,1 -k2,2n $coverage_file -o $coverage_file
        echo "Sort a file $coverage_file" >> $log
done


now=$(date)
echo "The build_coverages  script finished at $now" >> $log
