import matplotlib.pyplot as plt
import numpy as np

benchmarks = ("Load", "A", "B", "C", "D", "E", "F")
ops_per_sec = {
    'RocksDB': (10.48, 3.24, 4.28, 5.00, 10.69, 1.35, 5.57),
    'Autumn c=0.8': (8.93, 3.43, 3.69, 3.77, 6.23, .83, 3.15),
    'Autumn c=0.6': (8.97, 3.20, 4.00, 5.27, 11.22, 1.21, 4.47),
    'Autumn c=0.4': (9.27, 2.82, 3.36, 3.66, 12.02, 1.24, 4.63),
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
ax.set_title('Value Size: 1 Kb, DB Size: 80 Gb, T=10')
ax.set_xticks(x + 1.5 * width, benchmarks)
ax.legend(loc='upper center', ncols=3)
ax.set_ylim(bottom=0, top=1.5)

# plt.show()
plt.savefig('a-f.png', dpi=600)