#!/bin/bash

for file in direct-reads-and-writes/rocks*.txt; do
    num_reads=0
    num_updates=0
    num_inserts=0
    num_scans=0
    num_read_modify_writes=0

    read_lat=0
    update_lat=0
    insert_lat=0
    scan_lat=0
    read_modify_writes_lat=0

    echo ${file}
    # grep '^\[READ\], Operations,' ${file}
    num_reads=$(grep '\[READ\], Operations' ${file} | awk '{print $3}')
    read_lat=$(grep '\[READ\], AverageLatency(us),' ${file} | awk '{print $3}')

    num_updates=$(grep '\[UPDATE\], Operations' ${file} | awk '{print $3}')
    update_lat=$(grep '\[UPDATE\], AverageLatency(us),' ${file} | awk '{print $3}')

    num_inserts=$(grep '\[INSERT\], Operations' ${file} | awk '{print $3}')
    insert_lat=$(grep '\[INSERT\], AverageLatency(us),' ${file} | awk '{print $3}')

    num_scans=$(grep '\[SCAN\], Operations' ${file} | awk '{print $3}')
    scan_lat=$(grep '\[SCAN\], AverageLatency(us),' ${file} | awk '{print $3}')

    num_read_modify_writes=$(grep '\[SCAN\], Operations' ${file} | awk '{print $3}')
    read_modify_writes_lat=$(grep '\[SCAN\], AverageLatency(us),' ${file} | awk '{print $3}')

    # echo "read_lat = ${read_lat}, update_lat = ${update_lat}, insert_lat = ${insert_lat}, scan_lat = ${scan_lat}"
    
    if [ -n "$read_lat" ]; then
        read=$(python3 -c "print($num_reads * $read_lat)")
    else
        num_reads=0
        read=0
    fi

    if [ -n "$update_lat" ]; then
        update=$(python3 -c "print($num_updates * $update_lat)")
    else
        num_updates=0
        update=0
    fi

    if [ -n "$insert_lat" ]; then
        insert=$(python3 -c "print($num_inserts * $insert_lat)")
    else
        num_inserts=0
        insert=0
    fi

    if [ -n "$scan_lat" ] && [ -n $num_scans ]; then
        scan=$(python3 -c "print($num_scans * $scan_lat)")
    else
        num_scans=0
        scan=0
    fi

    if [ -n "$read_modify_write_lat" ] && [ -n $num_read_modify_writes ]; then
        read_modify_write=$(python3 -c "print($num_read_modify_writes * $read_modify_write_lat)")
    else
        num_read_modify_writes=0
        read_modify_write=0
    fi

    total_time=$(python3 -c "print(($read + $update + $insert + $scan + $read_modify_write))")
    total_ops=$(python3 -c "print($num_reads + $num_inserts + $num_updates + $num_scans + $num_read_modify_writes)")

    if (( ${total_time%.*} != 0 )); then
        result=$(python3 -c "print($total_ops / $total_time * 1000)")
        echo $result
    else
        echo ""
    fi
done