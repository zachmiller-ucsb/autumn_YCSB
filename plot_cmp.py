import matplotlib.pyplot as plt
import numpy as np

benchmarks = ("Load",)
ops_per_sec = {
    'RocksDB (T=3)': (10.0,),
    'RocksDB (T=5)': (9.9,),
    'RocksDB (T=7)': (9.0,),
    'RocksDB (T=10)': (9.2,),
}
colors = ['black', 'orange', 'blue', 'red']

x = np.arange(len(benchmarks))  # the label locations
width = 0.125  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

i = 0
for db, measurement in ops_per_sec.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, np.array(measurement)/np.array(ops_per_sec['RocksDB (T=5)']), width, label=db, color=colors[i], align='center')
    ax.bar_label(rects, padding=1, rotation='vertical', labels=measurement)
    multiplier += 1
    i += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Normalized Throughput')
# ax.set_title('Value Size: 1 Kb, DB Size: 80 Gb, T=5, Sleep 200 min')
ax.set_title('Value Size: 1 Kb, DB Size: 80 Gb, T=5')
ax.set_xticks(x + 1.5 * width, benchmarks)
ax.legend(loc='upper center', ncols=3)
ax.set_ylim(bottom=0, top=1.4)

# plt.show()
plt.savefig('a-f.png', dpi=600)