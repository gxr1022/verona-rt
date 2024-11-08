#!/bin/bash

base_dir="/users/Xuran/verona-rt/log"
date_folder=$1
work_dir="$base_dir/$date_folder"

for sub_dir in "$work_dir"/*; do
    if [ -d "$sub_dir" ]; then
        output_file="$sub_dir/run_time_diff_cores.csv"
        echo "cores,time" > "$output_file"

        for logfile in "$sub_dir"/*.log; do
            if [ -f "$logfile" ]; then
                cores=$(basename "$logfile" | sed 's/.*\.\([0-9]\+\)\.cores\..*/\1/')
                time_value=$(grep "Time so far:" "$logfile" | awk '{print $4}')
                echo "$cores,$time_value" >> "$output_file"
            fi
        done
        sort -t',' -k1,1n -o "$output_file" "$output_file"
    fi
done
