#!/bin/bash


tmpfile=$(mktemp)

declare -a latencies

for file in rocks/comp_*; do
    grep '^readrandom   :' ${file} | awk 'NR%2 == 0' | awk 'NR%3 == 0 {print $3}' >> $tmpfile
    echo ${file}
    grep '^readrandom   :' ${file} | awk 'NR%2 == 0' | awk 'NR%3 == 0 {print $3}'
done

python3 << EOF

import sys

with open('$tmpfile', 'r') as f:
    latencies = [float(line.strip()) for line in f]

# averages = [0] * 7
# counts = [0] * 7
# for i, latency in enumerate(latencies):
#     index = i % 7
#     averages[index] += latency
#     counts[index] += 1
average = sum(latencies)/len(latencies)
print("{:.3f}".format(average))

# for i, total in enumerate(averages):
#     if counts[i] > 0:
#         average = total / counts[i]
#         print("Index {}: {:.3f}".format(i, average))
EOF

rm $tmpfile