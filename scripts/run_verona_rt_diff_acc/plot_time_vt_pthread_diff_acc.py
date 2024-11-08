import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

boc_date = input("Enter BOC date (format: YYYY-MM-DD-HH-MM-SS): ")
pthread_date = input("Enter Pthread date (format: YYYY-MM-DD-HH-MM-SS): ")

base_path = '/users/Xuran/verona-rt/log'
boc_base = f'{base_path}/{boc_date}'
pthread_base = f'{base_path}/{pthread_date}'

acc_folders = glob.glob(f'{boc_base}/acc_*')

for acc_folder in acc_folders:
    acc_num = acc_folder.split('acc_')[-1]
    
    boc_file = f'{boc_base}/acc_{acc_num}/run_time_diff_cores.csv'
    pthread_file = f'{pthread_base}/acc_{acc_num}/run_time_diff_cores.csv'
    
    if not os.path.exists(boc_file) or not os.path.exists(pthread_file):
        print(f"Skip acc_{acc_num}: Files not found")
        continue
    
    boc_data = pd.read_csv(boc_file)
    pthread_data = pd.read_csv(pthread_file)
    
    plt.figure(figsize=(12, 8))
    
    plt.plot(boc_data['cores'], boc_data['time'], marker='o', label='BOC', linewidth=2)
    plt.plot(pthread_data['cores'], pthread_data['time'], marker='s', label='Pthread', linewidth=2)
    
    plt.title(f'BOC vs Pthread Performance Comparison on Busy Banking (acc_{acc_num})', fontsize=14)
    plt.xlabel('Hardware Threads', fontsize=12)
    plt.ylabel('Time Taken (ms)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    plt.xticks(range(0, max(boc_data['cores'].max(), pthread_data['cores'].max()) + 1, 4))
    
    plt.tight_layout()
    plt.savefig(f'acc{acc_num}_vt_pthread_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()