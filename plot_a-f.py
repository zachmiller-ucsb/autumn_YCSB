import matplotlib.pyplot as plt
import numpy as np

benchmarks = ("Load", "A", "B", "C", "D", "E", "F")
ops_per_sec = {
    'RocksDB': (0, .13, .30, .30, .33, .17, .15),
    'Autumn c=0.8': (0, .21, .31, .31, .33, .34, .31),
    'Autumn c=0.6': (0, .19, .33, .34, .37, .046, .33),
    'Autumn c=0.4': (0, .13, .36, .35, .26, .23, .33),
}
colors = ['black', 'orange', 'blue', 'red']

x = np.arange(len(benchmarks))  # the label locations
width = 0.125  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

i = 0
for db, measurement in ops_per_sec.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=db, color=colors[i], align='center')
    ax.bar_label(rects, padding=1, rotation='vertical')
    multiplier += 1
    i += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Throughput (K ops/sec)')
ax.set_title('Value Size: 1 Kb, DB Size: 80 Gb')
ax.set_xticks(x + 1.5 * width, benchmarks)
ax.legend(loc='upper center', ncols=3)
ax.set_ylim(bottom=0, top=.5)

plt.show()
# plt.savefig('YCSB_a-f.png', dpi=600)