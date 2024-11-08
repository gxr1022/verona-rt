import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import glob

if len(sys.argv) != 2:
    print("Usage: python plot_time_diff_worksec.py <datetime_path>")
    sys.exit(1)

datetime_path = sys.argv[1]
base_dir = f'/users/Xuran/verona-rt/log/{datetime_path}'

work_dirs = glob.glob(os.path.join(base_dir, 'work_usec_*'))

for work_dir in work_dirs:
    csv_path = os.path.join(work_dir, 'run_time_diff_cores.csv')
    if not os.path.exists(csv_path):
        print(f"Warning: File not found: {csv_path}")
        continue

    df = pd.read_csv(csv_path)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['cores'], df['time'], marker='o', linewidth=2, markersize=6)
    
    work_usec = os.path.basename(work_dir).split('_')[-1]
    plt.title(f'Runtime vs Hardware threads (Work: {work_usec}µs)', fontsize=14)
    plt.xlabel('Hardware threads', fontsize=12)
    plt.ylabel('Time Taken (ms)', fontsize=12)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_path = os.path.join(work_dir, 'run_time_diff_cores.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()