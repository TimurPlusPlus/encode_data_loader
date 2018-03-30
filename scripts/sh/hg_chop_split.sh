#!/bin/bash
chop_size="${1}"
hg19_path="${2}"
hg19_file_path=$hg19_path"hg19.bed"

cd $hg19_path
bedops --chop $chop_size $hg19_file_path | awk -F'\t' '{print>$1"_.bed"}'