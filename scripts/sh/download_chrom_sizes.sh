#!/bin/bash

hg_location=$1
fetchChromSizes=$2
sh "${fetchChromSizes}" hg19 | awk 'BEGIN{OFS="\t"}{print $1,"0",$2}' | sort-bed -> "${hg_location}"hg19.bed