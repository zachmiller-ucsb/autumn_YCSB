#!/bin/bash 

for file in rocks/comp_*; do
    echo ${file}
    # This line filters out the first read after load phase, and checks if there were any compactions 
    # in the data we want to use
    grep '^rocksdb\.compaction\.times\.micros' ${file} | awk 'NR%5 != 1' | grep -v '0$'
done