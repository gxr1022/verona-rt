#!/bin/bash
current=`date "+%Y-%m-%d-%H-%M-%S"`
RUN_PATH="/users/Xuran/verona-rt"
BINARY_PATH=${RUN_PATH}/build
threads=(1)
for ((i = 2; i <=40; i += 1)); do
    threads+=($i)
done


pushd ${BINARY_PATH}
cmake -B ${BINARY_PATH} -GNinja -DUSE_SYSTEMATIC_TESTING=OFF -DCMAKE_BUILD_TYPE=Release ${RUN_PATH}  2>&1 | tee ${RUN_PATH}/configure.log
if [[ "$?" != 0  ]];then
    exit
fi
ninja

# first group: the impact of work_usec 
num_trans=(100000) # 100k
# work_usec=(0 10 100)
work_usec=(1)
accounts=(1024) # concurrent cowner


TEST_PATH=${BINARY_PATH}/test
test_name=(perf-con-banking)

for work in ${work_usec[*]}; do
for trans in ${num_trans[*]}; do
for acc in ${accounts[*]}; do
    LOG_PATH=${RUN_PATH}/log/${current}/work_usec_${work}
    mkdir -p ${LOG_PATH}
    for t in ${threads[*]}; do
        for tn in ${test_name[*]}; do
            this_log_path=${LOG_PATH}/${tn}.${t}.cores.${acc}.acc.${trans}.trans.${work}.usec.log
            cmd="${TEST_PATH}/${tn}"
            
            echo "Running on cores: $cpu_list with accounts: $acc"
            echo ${cmd} 2>&1 | tee -a ${this_log_path}
            timeout -v 3600 stdbuf -o0 ${cmd} --cores ${t} --work_usec ${work} --num_trans ${trans} --accounts ${acc} 2>&1 | tee -a ${this_log_path}
            echo "Log file in: ${this_log_path}"
            echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 
        done
    done
done
done
done
popd

echo "Extracting timing data..."
${RUN_PATH}/scripts/run_verona_rt_diff_worksec/extract_time_diff_worksec.sh ${current}

echo "Generating plots..."
python3 ${RUN_PATH}/scripts/run_verona_rt_diff_worksec/plot_time_diff_worksec.py ${current}
