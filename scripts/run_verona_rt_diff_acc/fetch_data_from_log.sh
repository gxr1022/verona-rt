#!/bin/bash

RUN_PATH="/users/Xuran/verona-rt"
cur_date=$1

logs_folder="$RUN_PATH/log/$cur_date"
output_dir="$RUN_PATH/data/$cur_date"
mkdir -p "$output_dir"

tmp_file=$(mktemp)

if [ ! -d "$logs_folder" ]; then
    echo "Log folder $logs_folder does not exist"
    exit 1
fi

for acc in 32 64 128 256 512 1024; do
    output_file="$output_dir/banking_cores_time_acc${acc}_output.csv"
    echo "cores,time" > "$output_file"
    
    for file in "$logs_folder/acc${acc}"/perf-con-banking.*.cores.acc${acc}.log; do
        [ -f "$file" ] || continue
        
        cores=$(echo "$file" | grep -oP 'perf-con-banking.\K\d+(?=.cores)')
        time=$(grep -oP '(?<=Time so far: )\d+' "$file")
        
        if [ -n "$cores" ] && [ -n "$time" ]; then
            echo "$cores,$time" >> "$tmp_file"
        else
            echo "Warning: Missing data in $file" >&2
        fi
    done
    
    sort -g -t, -k1 "$tmp_file" >> "$output_file"
    > "$tmp_file"  # 清空临时文件以供下一个acc使用
    
    echo "Core counts for acc=$acc have been sorted and extracted to $output_file"
done

rm "$tmp_file"
