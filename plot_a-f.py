import matplotlib.pyplot as plt
import numpy as np

benchmarks = ("Load", "A", "B", "C", "D", "E", "F")
ops_per_sec = {
    'RocksDB': (11.22, 4.81, 6.30, 6.68, 13.63, 1.17, 5.14),
    'Autumn c=0.8': (9.16, 4.45, 5.58, 6.40, 13.06, 1.19, 5.16),
    'Autumn c=0.6': (9.95, 5.03, 7.40, 6.86, 13.13, 1.19, 5.30),
    'Autumn c=0.4': (8.69, 5.25, 6.76, 7.53, 14.80, 1.28, 5.77),
}
colors = ['black', 'orange', 'blue', 'red']

x = np.arange(len(benchmarks))  # the label locations
width = 0.125  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

i = 0
for db, measurement in ops_per_sec.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, np.array(measurement)/np.array(ops_per_sec['RocksDB']), width, label=db, color=colors[i], align='center')
    ax.bar_label(rects, padding=1, rotation='vertical', labels=measurement)
    multiplier += 1
    i += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Normalized Throughput')
ax.set_title('Value Size: 1 Kb, DB Size: 80 Gb, T=5, Sleep 50 min')
ax.set_xticks(x + 1.5 * width, benchmarks)
ax.legend(loc='upper center', ncols=3)
ax.set_ylim(bottom=0, top=1.5)

# plt.show()
plt.savefig('a-f.png', dpi=600)