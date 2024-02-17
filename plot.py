import re
import sys
import matplotlib.pyplot as plt
import numpy as np

def parse():
    START_LINE_REGEX = re.compile(r'\d\d\d\d-\d\d-\d\d')
    SECOND_REGEX = re.compile(r'(\d+) sec')
    OPERATION_REGEX = re.compile(r'READ|INSERT|UPDATE|SCAN|CLEANUP')
    PERCENTILE_REGEX_90 = re.compile(r' 90=(\d+)')
    PERCENTILE_REGEX_99 = re.compile(r' 99=(\d+)')

    with open(sys.argv[1]) as f:
        data = dict({'READ' : [[],[]], 'INSERT' : [[],[]], 'UPDATE' : [[],[]], 'SCAN' : [[],[]], 'CLEANUP' : [[],[]]})
        while line := f.readline():
            if re.match(START_LINE_REGEX, line):
                second_match = re.search(SECOND_REGEX, line)
                operation_match = re.findall(OPERATION_REGEX, line)
                percentile_90_match = re.findall(PERCENTILE_REGEX_90, line)
                percentile_99_match = re.findall(PERCENTILE_REGEX_99, line)

                if not operation_match:
                    continue
                for key in data.keys():
                    if int(second_match[1]) > 30:
                        if key not in operation_match:
                            data[key][0].append((int(second_match[1]), 0))
                            data[key][1].append((int(second_match[1]), 0))
                        else:
                            data[key][0].append((int(second_match[1]), int(percentile_90_match[operation_match.index(key)])))
                            data[key][1].append((int(second_match[1]), int(percentile_99_match[operation_match.index(key)])))
        # Handle case where we get duplicate timestamps
        for data_list in data.values():
            timestamps_90 = set()
            for time, latency in data_list[0]:
                if time in timestamps_90:
                    data_list[0].remove((time, latency))
                else:
                    timestamps_90.add(time)
            timestamps_99 = set()
            for time, latency in data_list[1]:
                if time in timestamps_99:
                    data_list[1].remove((time, latency))
                else:
                    timestamps_99.add(time)

        return data
    
def plot(filename, title, max_y, operations):
    data = parse()

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
    fig.suptitle(title)
    ax1.set_title("90th Percentile")
    ax2.set_title("99th Percentile")
    plt.ylim(0,max_y)

    legend_items = []
    for op, color in operations.items():
        scans_90, = ax1.plot(*zip(*data[op][0]), label=op, color=color)
        # ax1.axhline(y=np.median([l for t, l in data[op][0]]), color='black', linestyle='--')
        ax2.plot(*zip(*data[op][1]), label=op, color=color)
        # ax2.axhline(y=np.median([l for t, l in data[op][1]]), color='black', linestyle='--')
        legend_items.append(scans_90)
    fig.legend(handles=legend_items)

    plt.subplots_adjust(hspace=0.5)

    # Add common x and y axis labels, following https://stackoverflow.com/a/53172335
    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time (s)")
    plt.ylabel("Latency (micros)")

    plt.savefig(filename, dpi=600)

if __name__ == '__main__':
    c = 0.4
    # plot(f"scans/c{c}.png",f"Autumn on YCSB (c = {c})",(400,999), {'SCAN' : 'orange', 'INSERT' : 'blue'})
    plot("scans/rocks.png","RocksDB on YCSB",(400,999), {'SCAN' : 'orange', 'INSERT' : 'blue'})